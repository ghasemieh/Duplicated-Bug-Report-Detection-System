
import pandas as pd

def index_to_id(df, original_df):
    import time
    import progressbar as pb
    print('Convert index to id')
    start_time = time.time()
    progress = pb.ProgressBar(maxval=len(df)).start()
    progvar = 0

    for tup in df.itertuples():
        df.loc[tup.Index, 'id1'] = original_df.iloc[tup.id1]['id']
        df.loc[tup.Index, 'id2'] = original_df.iloc[tup.id2]['id']
        progress.update(progvar + 1)
        progvar += 1
    print("Index to id and Remove diff product score\n --- %s seconds ---" % (time.time() - start_time))


def index_to_id_remove_diff_product_score(df, original_df):
    import time
    import progressbar as pb
    print('Convert index to id and remove diff product score')
    start_time = time.time()
    progress = pb.ProgressBar(maxval=len(df)).start()
    progvar = 0

    for tup in df.itertuples():
        ID1 = original_df.iloc[tup.id1]['id']
        ID2 = original_df.iloc[tup.id2]['id']
        df.loc[tup.Index, 'id1'] = ID1
        df.loc[tup.Index, 'id2'] = ID2
        product1 = original_df.loc[lambda df: df['id'] == ID1, 'product'].array[0]
        product2 = original_df.loc[lambda df: df['id'] == ID2, 'product'].array[0]
        if product1 != product2:
            df.drop([tup.Index], inplace=True)
        progress.update(progvar + 1)
        progvar += 1
    print("Index to id and Remove diff product score\n --- %s seconds ---" % (time.time() - start_time))


def remove_diff_product_score(df, original_df):
    import time
    import progressbar as pb
    print('Remove record of diff product')
    start_time = time.time()
    progress = pb.ProgressBar(maxval=len(df)).start()
    progvar = 0

    for tup in df.itertuples():
        product1 = original_df.loc[lambda df: df['id'] == tup.id1, 'product'].array[0]
        product2 = original_df.loc[lambda df: df['id'] == tup.id2, 'product'].array[0]
        if product1 != product2:
            df.drop([tup.Index], inplace=True)
        progress.update(progvar + 1)
        progvar += 1
    print("Remove diff product score --- %s seconds ---" % (time.time() - start_time))


def id_builder(df):
    length = len(str(len(df)))
    ID = []
    for x in df.itertuples():
        ID1 = int(x.id1)
        ID2 = int(x.id2)
        ID.append(ID1 * pow(10, length) + ID2)
    ID_df = pd.DataFrame(ID, columns=['ID'])
    return pd.merge(df, ID_df, left_index=True, right_index=True)