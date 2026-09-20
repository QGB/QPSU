import time, sqlite3, threading, logging
from paho.mqtt import client as mqtt_client
from paho.mqtt.enums import CallbackAPIVersion

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

broker = 'broker-cn.emqx.io'
port = 1883
client_id = f'python_mqtt_client_{int(time.time())}'
DB_PATH = 'mqtt_messages.db'

class MQTTService:
    def __init__(self, broker='broker-cn.emqx.io', port=1883, client_id=client_id, log_messages=True):
        self.broker = broker
        self.port = port
        self.client_id = client_id
        self.client = None
        self.subscribed_topics = set()
        self.running = False
        self.log_messages = log_messages  #  新增：控制消息日志
        self._init_database()

    def _init_database(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mqtt_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                payload TEXT,
                qos INTEGER,
                retain INTEGER,
                received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_topic ON mqtt_messages(topic)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_received_at ON mqtt_messages(received_at)')
        self.conn.commit()
        logger.info(f"数据库初始化成功: {DB_PATH}")

    def _save_message(self, topic, payload, qos=0, retain=0):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO mqtt_messages (topic, payload, qos, retain) VALUES (?, ?, ?, ?)",
                          (topic, payload, qos, retain))
            self.conn.commit()
        except Exception as e:
            logger.error(f"保存消息失败: {e}")

    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            logger.info(f"成功连接到MQTT服务器: {self.broker}:{self.port}")
            self._resubscribe_all_topics()
        else:
            logger.error(f"连接失败，返回码: {rc}")

    def _resubscribe_all_topics(self):
        topics = list(self.subscribed_topics)
        if topics:
            logger.info(f"重新订阅 {len(topics)} 个主题: {topics}")
            for topic in topics:
                self.client.subscribe(topic)

    def on_message(self, client, userdata, msg):
        try:
            payload = msg.payload.decode('utf-8')
        except UnicodeDecodeError:
            payload = str(msg.payload)
        if self.log_messages:  #  根据配置决定是否打印
            logger.info(f"收到消息 - 主题: {msg.topic}, 内容: {payload[:200]}")
        if 'Chonburi' in payload:return
        self._save_message(topic=msg.topic, payload=payload, qos=msg.qos, retain=msg.retain)

    def on_disconnect(self, client, userdata, flags, reasonCode, properties=None):
        if reasonCode != 0:
            logger.warning(f"意外断开连接，reasonCode={reasonCode}，将尝试重连...")
            self._start_reconnect_thread()

    def _start_reconnect_thread(self):
        if self.running:
            thread = threading.Thread(target=self._reconnect_loop, daemon=True)
            thread.start()

    def _reconnect_loop(self):
        delay = 1
        while self.running and not self.client.is_connected():
            try:
                logger.info(f"尝试重连，延迟 {delay} 秒...")
                time.sleep(delay)
                self.client.reconnect()
                delay = min(delay * 2, 60)
            except Exception as e:
                logger.error(f"重连失败: {e}")

    def connect(self):
        try:
            self.client = mqtt_client.Client(CallbackAPIVersion.VERSION2, client_id=self.client_id, protocol=mqtt_client.MQTTv311)
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            self.client.on_disconnect = self.on_disconnect
            self.client.connect(self.broker, self.port)
            self.running = True
            self.client.loop_start()
            logger.info("MQTT客户端已启动")
            return True
        except Exception as e:
            logger.error(f"连接失败: {e}")
            return False

    def subscribe(self, topic, qos=0):
        if not self.client:
            logger.error("客户端未初始化，请先调用connect()")
            return False
        try:
            result, mid = self.client.subscribe(topic, qos)
            if result == mqtt_client.MQTT_ERR_SUCCESS:
                self.subscribed_topics.add(topic)
                logger.info(f"订阅主题成功: {topic} (QoS={qos})")
                return True
            else:
                logger.error(f"订阅主题失败: {topic}, 错误码: {result}")
                return False
        except Exception as e:
            logger.error(f"订阅主题异常: {e}")
            return False

    def subscribe_list(self, *topics):
        """批量订阅主题，支持传入 (topic, qos) 元组或直接传入 topic 使用默认 qos=0"""
        if not self.client:
            logger.error("客户端未初始化，请先调用connect()")
            return False
        success = True
        for item in topics:
            if isinstance(item, tuple) and len(item) == 2:
                topic, qos = item
            else:
                topic, qos = item, 0
            try:
                result, mid = self.client.subscribe(topic, qos)
                if result == mqtt_client.MQTT_ERR_SUCCESS:
                    self.subscribed_topics.add(topic)
                    logger.info(f"订阅主题成功: {topic} (QoS={qos})")
                else:
                    logger.error(f"订阅主题失败: {topic}, 错误码: {result}")
                    success = False
            except Exception as e:
                logger.error(f"订阅主题异常: {topic}, {e}")
                success = False
        return success

    def unsubscribe(self, topic):
        if not self.client:
            logger.error("客户端未初始化")
            return False
        try:
            result, mid = self.client.unsubscribe(topic)
            if result == mqtt_client.MQTT_ERR_SUCCESS:
                if topic in self.subscribed_topics:
                    self.subscribed_topics.remove(topic)
                logger.info(f"取消订阅成功: {topic}")
                return True
            else:
                logger.error(f"取消订阅失败: {topic}, 错误码: {result}")
                return False
        except Exception as e:
            logger.error(f"取消订阅异常: {e}")
            return False

    def publish(self, topic, payload, qos=0, retain=False):
        if not self.client:
            logger.error("客户端未初始化")
            return False
        try:
            result, mid = self.client.publish(topic, payload, qos, retain)
            if result == mqtt_client.MQTT_ERR_SUCCESS:
                if self.log_messages:  #  发布日志也可选
                    logger.info(f"发布消息成功 - 主题: {topic}, 内容: {payload[:100]}")
                return True
            else:
                logger.error(f"发布消息失败: {topic}, 错误码: {result}")
                return False
        except Exception as e:
            logger.error(f"发布消息异常: {e}")
            return False

    def get_subscribed_topics(self):
        return list(self.subscribed_topics)

    def query_messages(self, topic=None, limit=100):
        try:
            cursor = self.conn.cursor()
            if topic:
                cursor.execute("SELECT id, topic, payload, received_at FROM mqtt_messages WHERE topic = ? ORDER BY received_at DESC LIMIT ?", (topic, limit))
            else:
                cursor.execute("SELECT id, topic, payload, received_at FROM mqtt_messages ORDER BY received_at DESC LIMIT ?", (limit,))
            return cursor.fetchall()
        except Exception as e:
            logger.error(f"查询消息失败: {e}")
            return []

    #  新增：统计每个topic的消息总数、最后一条消息内容和时间
    def get_topic_stats(self, topic=None):
        try:
            cursor = self.conn.cursor()
            if topic is not None:
                cursor.execute("SELECT COUNT(*) FROM mqtt_messages WHERE topic = ?", (topic,))
                count = cursor.fetchone()[0]
                if count > 0:
                    cursor.execute("SELECT payload, received_at FROM mqtt_messages WHERE topic = ? ORDER BY received_at DESC LIMIT 1", (topic,))
                    last_payload, last_time = cursor.fetchone()
                    return {topic: {"count": count, "last_payload": last_payload, "last_time": last_time}}
                else:
                    return {topic: {"count": 0, "last_payload": None, "last_time": None}}
            else:
                cursor.execute("""
                    SELECT topic, COUNT(*) as cnt,
                        (SELECT payload FROM mqtt_messages t2 WHERE t2.topic = t1.topic ORDER BY received_at DESC LIMIT 1) as last_payload,
                        (SELECT received_at FROM mqtt_messages t2 WHERE t2.topic = t1.topic ORDER BY received_at DESC LIMIT 1) as last_time
                    FROM mqtt_messages t1
                    GROUP BY topic
                """)
                rows = cursor.fetchall()
                stats = {}
                for row in rows:
                    stats[row[0]] = {"count": row[1], "last_payload": row[2], "last_time": row[3]}
                return stats
        except Exception as e:
            logger.error(f"获取topic统计失败: {e}")
            return {} if topic is None else {topic: {"count": 0, "last_payload": None, "last_time": None}}

    #  新增：动态开关消息日志
    def set_log_messages(self, enable: bool):
        self.log_messages = enable
        logger.info(f"MQTT消息内容日志已{'开启' if enable else '关闭'}")

    def stop(self):
        self.running = False
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
            logger.info("MQTT客户端已停止")
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()

# 使用示例（与您的测试完全相同，额外演示统计功能）
if __name__ == "__main__":
    mqtt=MQTTService(broker='broker-cn.emqx.io', port=1883, log_messages=True)
    mqtt.connect()
    time.sleep(1)
    mqtt.subscribe_list('topic','test','test/topic','hello','hello/world','mqtt','msg','sys')
    mqtt.publish("test", "Hello MQTT")
    time.sleep(5)
    # U.sleep(5)
    mqtt.set_log_messages(0)