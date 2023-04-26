import boto3
import sys
import json
import argparse

def list_tables(br_session, tag):
    dynamodb_client_br = br_session.client("dynamodb")
    tables = []
    full_list_tables = dynamodb_client_br.list_tables()
    for table in full_list_tables["TableNames"]:
        table_arn = dynamodb_client_br.describe_table(TableName=table)['Table']['TableArn']
        if tag in dynamodb_client_br.list_tags_of_resource(ResourceArn=table_arn)['Tags']:
            tables.append(table)
    return tables

def create_backups(br_session, tables):
    try:
        dynamodb_client_br = br_session.client("dynamodb")
        backups = []
        for table in tables:
            print("Backuping {} in sa-east-1...".format(table))
            backups.append({
                "TableName": table, 
                "BackupArn": dynamodb_client_br.create_backup(TableName=table,BackupName=table)["BackupDetails"]["BackupArn"]
            })
        return backups
    except Exception as e:
        print(e)

def restore_backups(us_session, backups):
    try:
        us_tables = []
        dynamodb_client_us = us_session.client("dynamodb")
        for backup in backups:
            print("Restoring {} in us-east-1...".format(backup["TableName"]))
            response = dynamodb_client_us.restore_table_from_backup(
                TargetTableName=backup["TableName"],
                BackupArn=backup["BackupArn"],
                SSESpecificationOverride={
                    "Enabled": False
                }
            )
            print("Table {} created from restore in us-east-1!".format(response["TableDescription"]["TableArn"]))
            us_tables.append(response["TableDescription"]["TableArn"])
        return us_tables
    except Exception as e:
        print(e)

def lambda_handler(event, context):
    try:
        tag = event
        br_session = boto3.Session(region_name="sa-east-1")
        us_session = boto3.Session(region_name="us-east-1")
        tables = list_tables(br_session, tag)
        backups = create_backups(br_session, tables)
        us_tables = restore_backups(us_session, backups)
        print("TABLES CREATED IN US: {}".format(us_tables))
    except Exception as e:
        print(e)