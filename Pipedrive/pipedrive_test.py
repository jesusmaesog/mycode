from pipedrive.client import Client
import json
import pandas as pd
import random
import faker
import os
import pyodbc
import numpy as np
from dotenv import load_dotenv
from pykeepass import PyKeePass

# Initialize Faker for generating random data
# fake = faker.Faker()

# # Generate 100 random entries for each column
# names = [fake.first_name() for _ in range(100)]
# surnames = [fake.last_name() for _ in range(100)]
# phones = [fake.phone_number() for _ in range(100)]
# emails1 = [fake.email() for _ in range(100)]
# emails2 = [fake.email() for _ in range(100)]
# companies = [fake.company() for _ in range(100)]
# addresses = [fake.address().replace("\n", ", ") for _ in range(100)]
# projects = [fake.catch_phrase() for _ in range(100)]
# amounts = [random.randint(500000, 1500000) for _ in range(100)]

# Create a DataFrame with the generated data
# data = {
#     "Nombre": names,
#     "Apellido": surnames,
#     "Teléfono": phones,
#     "Email 1": emails1,
#     "Email 2": emails2,
#     "Empresa": companies,
#     "Dirección": addresses,
#     "Proyecto": projects,
#     "Importe (€)": amounts,
# }

# df = pd.DataFrame(data)
# df

#df.to_csv('C:/Users/jesus/OneDrive/Documents/Proyectos/Pipedrive/dababasepipedrive.csv', sep= ",", header= True, )

# Cargar las variables del archivo .env
load_dotenv(dotenv_path="C:/Users/jesus/OneDrive/Documents/Proyectos/Pipedrive/config/file.env")

# Obtener las variables del archivo .env
master_password = os.getenv("KEEPASS_MASTER_PASSWORD")
api_token = os.getenv("API_TOKEN")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

if not master_password or not api_token or not client_id or not client_secret:
    raise ValueError("Una o más variables de entorno no se cargaron correctamente.")

# Usar la contraseña maestra para abrir la base de datos KeePass
db_path = 'C:/Users/jesus/OneDrive/Documents/Proyectos/mycode/Pipedrive/Pipedrive_keepass.kdbx' 
password=master_password

# Cargar la base de datos
kp = PyKeePass(db_path, password=master_password)

# Acceder a las entradas y obtener los valores de las credenciales
client_id = kp.find_entries(title="ClientID", first=True).password
client_secret = kp.find_entries(title="Clientsecret", first=True).password
code = kp.find_entries(title="code", first=True).password
domain = kp.find_entries(title="domain", first=True).password
domain_deal = kp.find_entries(title="domain_deal", first=True).password
folder_path = kp.find_entries(title="folder_path", first=True).password
folder_path_bronze = kp.find_entries(title="folder_path_bronze", first=True).password
folder_path_silver = kp.find_entries(title="folder_path_silver", first=True).password
server = kp.find_entries(title="server", first=True).password
database = kp.find_entries(title="database", first=True).password
table_name1 = kp.find_entries(title="table_name1", first=True).password
table_name2 = kp.find_entries(title="table_name2", first=True).password
table_name3 = kp.find_entries(title="table_name3", first=True).password
api_token = kp.find_entries(title="api_token", first=True).password

cliente = Client(client_id, client_secret, domain)
cliente.set_api_token(api_token)
users = cliente.users.get_all_users()
deals = cliente.deals.get_all_deals()
organizations = cliente.organizations.get_all_organizations()
persons = cliente.persons.get_all_persons()

def export_pipedrive_data(folder_path_bronze, cliente):
    """
    Exporta datos de Pipedrive a archivos JSON en la carpeta especificada.

    Parameters:
        folder_path (str): Ruta a la carpeta donde se guardarán los archivos.
        client: Instancia del cliente Pipedrive.

    Returns:
        None
    """
    # Crear la carpeta si no existe
    os.makedirs(folder_path_bronze, exist_ok=True)

    # Diccionario con los endpoints y nombres de archivos
    endpoints = {
        "users": cliente.users.get_all_users(),
        "deals": cliente.deals.get_all_deals(),
        "organizations": cliente.organizations.get_all_organizations(),
        "persons": cliente.persons.get_all_persons()
    }

    for name, data in endpoints.items():
        # Construir la ruta completa para cada archivo JSON
        file_path = os.path.join(folder_path_bronze, f"{name}.json")

        # Guardar el archivo JSON
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        print(f"File {name}.json saved into: {file_path}")


export_pipedrive_data(folder_path_bronze, cliente)

# Primero vamos a guardar el data en una variable data por si acaso

data = persons["data"]

# Vamos a aplanar el data del json

df = pd.json_normalize(persons["data"])

# Expandir la columna 'email' y 'phone' para obtener un sendos DataFrame con registros separados y con un id que luego nos permita hacer un inner join en SSIS
# Normalización de datos
df_email = pd.json_normalize(data, 'email', ['id', 'name']).rename(columns={'value': 'email'})
df_phone = pd.json_normalize(data, 'phone', ['id', 'name']).rename(columns={'value': 'Phone.Phone_number'})


# Lista de dataframes a exportar
df_export_csv = {
    "df": df,
    "df_email": df_email,
    "df_phone": df_phone,
}

# Exportación de los dataframes a archivos CSV
for name, df in df_export_csv.items():
    file_path = f"{folder_path_silver}/{name}.csv"  # Generar un nombre de archivo dinámico
    df.to_csv(file_path, sep=',', header=True, index=False)
    print(f"Archivo exportado: {file_path}")


    

#Vamos a crear una base de datos que nos servirá como Datawarehouse o almacén para la explotación analítica de los datos.

# Conexión inicial a SQL Server
connection_string = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=JESUSMAESOG_PC;"  # Cambia a tu servidor
    "Trusted_Connection=yes;"  # Habilita autenticación de Windows
)

# Conectar al servidor
connection = pyodbc.connect(connection_string, autocommit=True)
cursor = connection.cursor()

# Crear la base de datos si no existe
cursor.execute(f"""
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = '{database}')
BEGIN
    CREATE DATABASE {database};
END
""")
connection.commit()
print("Base de datos verificada o creada exitosamente.")


##############################################################################################
# Conexión a la base de datos
connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_Connection=yes;"
)

try:
    conn = pyodbc.connect(connection_string, autocommit=True)
    cursor = conn.cursor()
    print(f"Conectado a la base de datos '{database}' exitosamente.")
except pyodbc.Error as e:
    print(f"Error al conectar a la base de datos: {e}")
    raise

# Función para crear tablas si no existen
def create_table_if_not_exists(table_name, create_sql):
    try:
        cursor.execute(f"""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name = ? AND xtype = 'U')
        BEGIN
            {create_sql}
        END;
        """, table_name)
        conn.commit()
        print(f"Tabla '{table_name}' creada o verificada exitosamente.")
    except pyodbc.Error as e:
        print(f"Error al crear/verificar la tabla '{table_name}': {e}")
        raise

# Crear la tabla principal (tabla1)
df_data_columns = [
    'id', 'company_id', 'name', 'first_name', 'last_name', 'open_deals_count', 'related_open_deals_count',
    'closed_deals_count', 'related_closed_deals_count', 'participant_open_deals_count', 'participant_closed_deals_count',
    'email_messages_count', 'activities_count', 'done_activities_count', 'undone_activities_count', 'files_count',
    'notes_count', 'followers_count', 'won_deals_count', 'related_won_deals_count', 'lost_deals_count',
    'related_lost_deals_count', 'active_flag', 'first_char', 'update_time', 'delete_time', 'add_time', 'visible_to',
    'picture_id', 'next_activity_date', 'next_activity_time', 'next_activity_id', 'last_activity_id', 'last_activity_date',
    'last_incoming_mail_time', 'last_outgoing_mail_time', 'label', 'postal_address', 'postal_address_lat',
    'postal_address_long', 'postal_address_subpremise', 'postal_address_street_number', 'postal_address_route',
    'postal_address_sublocality', 'postal_address_locality', 'postal_address_admin_area_level_1',
    'postal_address_admin_area_level_2', 'postal_address_country', 'postal_address_postal_code',
    'postal_address_formatted_address', 'notes', 'birthday', 'job_title', 'org_name', 'owner_name', 'primary_email',
    'cc_email', 'owner_id_id', 'owner_id_name', 'owner_id_email', 'owner_id_has_pic', 'owner_id_pic_hash',
    'owner_id_active_flag', 'owner_id_value', 'org_id_name', 'org_id_people_count', 'org_id_owner_id', 'org_id_address',
    'org_id_label_ids', 'org_id_active_flag', 'org_id_cc_email', 'org_id_owner_name', 'org_id_value'
]

column_types = {
    'id': 'INT PRIMARY KEY NOT NULL',
    'company_id': 'INT NOT NULL',
    'name': 'NVARCHAR(100)',
    'first_name': 'NVARCHAR(100)',
    'last_name': 'NVARCHAR(100)',
    'open_deals_count': 'INT',
    'related_open_deals_count': 'INT',
    'closed_deals_count': 'INT',
    'related_closed_deals_count': 'INT',
    'participant_open_deals_count': 'INT',
    'participant_closed_deals_count': 'INT',
    'email_messages_count': 'INT',
    'activities_count': 'INT',
    'done_activities_count': 'INT',
    'undone_activities_count': 'INT',
    'files_count': 'INT',
    'notes_count': 'INT',
    'followers_count': 'INT',
    'won_deals_count': 'INT',
    'related_won_deals_count': 'INT',
    'lost_deals_count': 'INT',
    'related_lost_deals_count': 'INT',
    'active_flag': 'BIT',
    'first_char': 'CHAR(1)',
    'update_time': 'DATETIME',
    'delete_time': 'DATETIME',
    'add_time': 'DATETIME',
    'visible_to': 'NVARCHAR(50)',
    'picture_id': 'INT',
    'next_activity_date': 'DATETIME',
    'next_activity_time': 'DATETIME',
    'next_activity_id': 'INT',
    'last_activity_id': 'INT',
    'last_activity_date': 'DATETIME',
    'last_incoming_mail_time': 'DATETIME',
    'last_outgoing_mail_time': 'DATETIME',
    'label': 'NVARCHAR(50)',
    'postal_address': 'NVARCHAR(255)',
    'postal_address_lat': 'FLOAT',
    'postal_address_long': 'FLOAT',
    'postal_address_subpremise': 'NVARCHAR(50)',
    'postal_address_street_number': 'NVARCHAR(50)',
    'postal_address_route': 'NVARCHAR(50)',
    'postal_address_sublocality': 'NVARCHAR(50)',
    'postal_address_locality': 'NVARCHAR(50)',
    'postal_address_admin_area_level_1': 'NVARCHAR(50)',
    'postal_address_admin_area_level_2': 'NVARCHAR(50)',
    'postal_address_country': 'NVARCHAR(50)',
    'postal_address_postal_code': 'NVARCHAR(20)',
    'postal_address_formatted_address': 'NVARCHAR(255)',
    'notes': 'NVARCHAR(255)',
    'birthday': 'DATETIME',
    'job_title': 'NVARCHAR(100)',
    'org_name': 'NVARCHAR(100)',
    'owner_name': 'NVARCHAR(100)',
    'primary_email': 'NVARCHAR(100)',
    'cc_email': 'NVARCHAR(100)',
    'owner_id_id': 'INT NOT NULL',
    'owner_id_name': 'NVARCHAR(100)',
    'owner_id_email': 'NVARCHAR(100)',
    'owner_id_has_pic': 'BIT',
    'owner_id_pic_hash': 'NVARCHAR(50)',
    'owner_id_active_flag': 'BIT',
    'owner_id_value': 'INT',
    'org_id_name': 'NVARCHAR(100)',
    'org_id_people_count': 'INT',
    'org_id_owner_id': 'INT',
    'org_id_address': 'NVARCHAR(255)',
    'org_id_label_ids': 'NVARCHAR(100)',
    'org_id_active_flag': 'BIT',
    'org_id_cc_email': 'NVARCHAR(100)',
    'org_id_owner_name': 'NVARCHAR(100)',
    'org_id_value': 'INT'
}

# Crear la tabla
columns_sql = ",\n".join([f"{col} {column_types.get(col, 'NVARCHAR(100)')}" for col in df_data_columns])
create_persons_sql = f"""
CREATE TABLE {table_name1} (
    {columns_sql}
);
"""

create_table_if_not_exists(table_name1, create_persons_sql)

# Crear tabla2
e_table_sql = f"""
CREATE TABLE {table_name2} (
    id INT PRIMARY KEY NOT NULL,
    label NVARCHAR(50),
    email NVARCHAR(50),
    primary_field BIT,
    persons_name_id INT NOT NULL,
    persons_name NVARCHAR(255)
);
"""
create_table_if_not_exists(table_name2, e_table_sql)

# Crear tabla3
p_table_sql = f"""
CREATE TABLE {table_name3} (
    id INT PRIMARY KEY NOT NULL,
    Phone NVARCHAR(25),
    primary_field BIT,
    persons_name_id INT NOT NULL,
    persons_name NVARCHAR(255)            
);
"""
create_table_if_not_exists(table_name3, p_table_sql)
