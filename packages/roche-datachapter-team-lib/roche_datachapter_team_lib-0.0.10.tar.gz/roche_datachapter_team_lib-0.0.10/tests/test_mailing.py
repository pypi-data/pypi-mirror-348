"""Test module for mailing module."""
import os
from roche_datachapter_team_lib.db_config import DB_CONFIG
from roche_datachapter_team_lib.query_manager import QueryManager
from roche_datachapter_team_lib.result_type import ResultType
from roche_datachapter_team_lib.excel_service import ExcelFile
from roche_datachapter_team_lib.email_service import EmailService, AttachmentFile, EmailDestination

QUERIES_DIR = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'queries')
QUERY_MANAGER = QueryManager(QUERIES_DIR)


query_latam_ar = QUERY_MANAGER.get_query('ej_latam_ar.sql')
df_usuarios_rdi = DB_CONFIG.execute_custom_select_query(
    query_latam_ar, "sqlserver_latam_ar", result_set_as=ResultType.PANDAS_DATA_FRAME)

query_rexis = QUERY_MANAGER.get_query('ej_rexis.sql')
df_usuarios_rexis = DB_CONFIG.execute_custom_select_query(
    query_rexis, "rexis_sales", result_set_as=ResultType.PANDAS_DATA_FRAME)


# get current file path directory
current_file_path_dir = os.path.dirname(os.path.realpath(__file__))
file_name_rdi = 'query_latam_ar'
excel_file_rdi = ExcelFile(os.path.join(current_file_path_dir, file_name_rdi))
excel_file_rdi.append_sheet_from_df(df_usuarios_rdi)
excel_file_rdi.save()

file_name_rexis = 'query_rexis.xlsx'
excel_file_rexis = ExcelFile(os.path.join(
    current_file_path_dir, file_name_rexis))
excel_file_rexis.append_sheet_from_df(df_usuarios_rexis)
excel_file_rexis.save()

file_name_merge = 'latam_ar_rexis.xlsx'
excel_file_merge = ExcelFile(os.path.join(
    current_file_path_dir, file_name_merge))
excel_file_merge.append_sheet_from_df(df_usuarios_rdi)
excel_file_merge.append_sheet_from_df(df_usuarios_rexis)
excel_file_merge.save()

destinatarios = EmailDestination(
    ['lucas.frias@roche.com'], ['uciel.bustamante@contractors.roche.com'], ['sara.fernandez.sf1@roche.com'])
attachments = [AttachmentFile(excel_file_rdi.get_destination_path()), AttachmentFile(
    excel_file_rexis.get_destination_path()), AttachmentFile(excel_file_merge.get_destination_path()),
    AttachmentFile(os.path.join(
                   current_file_path_dir, 'archivo.pdf')), ]

subject = 'Test solo to, cc, y bcc'
body = 'Esto es una prueba de envío de email desde roche_datachapter_lib'
EmailService().send_email(destinatarios, subject, body, attachments)

excel_file_merge.remove()
excel_file_rdi.remove()
excel_file_rexis.remove()