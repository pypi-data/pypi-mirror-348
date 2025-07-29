import boto3
import boto3.session
import glob
import os
import urllib3

urllib3.disable_warnings()

def conexao_s3():
    session = boto3.session.Session(aws_access_key_id=os.getenv("DETIC_ACCESS_KEY_ID"),
                                    aws_secret_access_key=os.getenv("DETIC_SECRET_ACCESS_KEY"))
    endpoint = 'https://s3.nuvem.unicamp.br'
    s3 = session.resource(service_name='s3', endpoint_url=endpoint, verify=False)
    return s3

def listar_objetos_s3(sessao,bucket_name):
    client = sessao.meta.client
    bucket = sessao.Bucket(bucket_name)
    registros = []
    lista = bucket.objects.all()
    for o in lista:
        #capturando metadados do objeto
        response = sessao.Object(bucket_name, o.key).get()
        linha = {}
        linha['bucket'] = bucket
        linha['nome_objeto'] = o.key
        linha['tamanho_objeto'] = o.size
        lista = tuple(linha.values())
        registros.append(lista)

    return registros

def upload_objetos_s3(sessao, bucket, origem, destino):
    rel_paths = glob.glob(origem + '/**', recursive=True)
    for local_file in rel_paths:
        if not os.path.isdir(local_file):
            local_file_linux = local_file.replace(os.sep, "/")
            if destino == '/':
                destino = ''
            sessao.Object(bucket, destino + local_file_linux[0 + len(origem):]).upload_file(
                local_file)
            
def deletar_objetos_s3(sessao,bucket, diretorio):
    for o in sessao.Bucket(bucket).objects.filter(Prefix='/' + diretorio):
        print(o.key)
        sessao.Object(bucket, o.key).delete()

def download_objeto_s3(sessao, bucket, arquivo, diretorio):
    path = diretorio + arquivo
    sessao.Object(bucket, arquivo).download_file(path)