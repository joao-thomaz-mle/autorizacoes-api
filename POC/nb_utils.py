import pandas as pd


def get_ids_and_blobs(df: pd.DataFrame) -> dict:
    ids_and_blobs = {}
    for index, row in df.iterrows():
        ids_and_blobs[row["CD_AVISO_CIRURGIA"]] = row["CD_DOCUMENTO_ANEXO_CIRURGICO"]
    return ids_and_blobs
