import gspread
from oauth2client.service_account import ServiceAccountCredentials


scope = ['https://spreadsheets.google.com/feeds']
path_to_json = U.gst+r'qgb-gapp-542f32f324b6.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(path_to_json, scope)
gc = gspread.authorize(credentials)


