import numpy as np


#########################################  MATRICES F & S FUNCTIONS  #########################################

def get_Trains_Dictionary(trains_list):
    '''
    This function gets list of trains as argument and then divides trains and their
    stops; trains are put into dictionary as keys and list of train's stops are
    values for each train.
    '''

    data = {}
    for train in trains_list:
        stop_names = []

        for stop in train.stops:
            stop_names.append(stop.stop_name)

        data.__setitem__(train.train_name, stop_names)

    return data

def get_Segments(data, trains):

    '''
    This function calculates every segment on a railway network and
    then returns sorted list of those segments. It gets two arguments;
    'data' which is dictionary where trains are keys and lists of each trains
    stations are values and 'trains' which is list of trains.
    '''

    segments = []

    for train in trains:
        route = data.get(train)
        for i in range(0, len(route)):
            if (i != (len(route) - 1)):
                if (route[i] > route[i+1]):
                    segment = route[i+1] + route[i]
                else:
                    segment = route[i] + route[i+1]
            else:
                if (route[i] > route[0]):
                    segment = route[0] + route[i]
                else:
                    segment = route[i] + route[0]

            if (segment in segments):
                continue
            else:
                segments.append(segment)

    segments.sort()
    return segments

def get_Trains_On_Segments(data, trains):

    '''
    This function is used for making strings that represent trains on
    their segments and then returns it as a list. It gets two arguments;
    'data' which is dictionary where trains are keys and lists of each trains
    stations are values and 'trains' which is list of trains.
    '''

    trains_on_segments = []

    for train in trains:
        route = data.get(train)
        for i in range(0, len(route)):
            if (i != (len(route) - 1)):
                if (route[i] > route[i+1]):
                    segment = route[i+1] + route[i]
                else:
                    segment = route[i] + route[i+1]
            else:
                if (route[i] > route[0]):
                    segment = route[0] + route[i]
                else:
                    segment = route[i] + route[0]

            segment = train + segment
            trains_on_segments.append(segment)

    return trains_on_segments

def get_Matrix_F(data, trains, segments, trains_on_segments):

    '''
    This function calculates and returns matirx F. It gets four arguments;
    'data' which is dictionary where trains are keys and lists of each trains
    stations are values, 'trains' which is list of trains, 'segments' which is
    list of all segments between stations and 'trains_on_segments' which is
    list of every train on its every segment.
    '''

    num_rows = len(trains)
    num_column_Fv = 0
    num_column_Fu = len(trains)
    num_column_Fr = len(get_Segments(data, trains))

    for train in trains:
        num_column_Fv = num_column_Fv + len(data.get(train))
        num_rows = num_rows + len(data.get(train))

    Fv = np.zeros((num_rows, num_column_Fv))
    Fr = np.zeros((num_rows, num_column_Fr))
    Fu = np.zeros((num_rows, num_column_Fu))
    Fy = np.zeros((num_rows, num_column_Fu))

    # matrix Fu
    for train in trains:
        if (trains.index(train) == 0):
            Fu[0][trains.index(train)] = 1
        else:
            cnt = 0
            for i in range(0, trains.index(train)):
                cnt = cnt + len(data.get(trains[i])) + 1

            Fu[cnt][trains.index(train)] = 1

    # matrix Fr
    cnt = 0
    for train in trains:
        route = data.get(train)

        for i in range(0, len(route)):
            if (i != (len(route) - 1)):
                if (route[i] > route[i+1]):
                    segment = route[i+1] + route[i]
                else:
                    segment = route[i] + route[i+1]
            else:
                if (route[i] > route[0]):
                    segment = route[0] + route[i]
                else:
                    segment = route[i] + route[0]

            Fr[cnt][segments.index(segment)] = 1
            cnt = cnt + 1

        cnt = cnt + 1

    # matrix Fv
    cnt = 1
    for train in trains:
        route = data.get(train)

        for i in range(0, len(route)):
            if (i != (len(route) - 1)):
                if (route[i] > route[i+1]):
                    segment = route[i+1] + route[i]
                else:
                    segment = route[i] + route[i+1]
            else:
                if (route[i] > route[0]):
                    segment = route[0] + route[i]
                else:
                    segment = route[i] + route[0]

            segment = train + segment
            Fv[cnt][trains_on_segments.index(segment)] = 1
            cnt = cnt + 1

        cnt = cnt + 1

    # matrica F = [Fu Fv Fr Fy]
    F = np.concatenate((Fu, Fv, Fr, Fy), axis=1)

    Fu = Fu.astype(int)
    Fv = Fv.astype(int)
    Fr = Fr.astype(int)
    Fy = Fy.astype(int)
    F = F.astype(int)

    return [F, Fu, Fv, Fr, Fy]

def get_Matrix_S(data, trains, segments, trains_on_segments):

    '''
    This function calculates and returns matirx S. It gets four arguments;
    'data' which is dictionary where trains are keys and lists of each trains
    stations are values, 'trains' which is list of trains, 'segments' which is
    list of all segments between stations and 'trains_on_segments' which is
    list of every train on its every segment.
    '''

    num_columns = len(trains)
    num_rows_Sv = 0
    num_rows_Sy = len(trains)
    num_rows_Sr = len(get_Segments(data, trains))

    for train in trains:
        num_rows_Sv = num_rows_Sv + len(data.get(train))
        num_columns = num_columns + len(data.get(train))

    Sv = np.zeros((num_rows_Sv, num_columns))
    Sr = np.zeros((num_rows_Sr, num_columns))
    Su = np.zeros((num_rows_Sy, num_columns))
    Sy = np.zeros((num_rows_Sy, num_columns))

    # matrix Sy
    for train in trains:
        if (trains.index(train) == 0):
            Sy[0][len(data.get(train))] = 1
        else:
            cnt = 0
            for i in range(0, trains.index(train)):
                cnt = cnt + len(data.get(trains[i])) + 1

            Sy[trains.index(train)][cnt + len(data.get(train))] = 1

    # matrix Sr
    cnt = 1
    for train in trains:
        route = data.get(train)

        for i in range(0, len(route)):
            if (i != (len(route) - 1)):
                if (route[i] > route[i+1]):
                    segment = route[i+1] + route[i]
                else:
                    segment = route[i] + route[i+1]
            else:
                if (route[i] > route[0]):
                    segment = route[0] + route[i]
                else:
                    segment = route[i] + route[0]

            Sr[segments.index(segment)][cnt] = 1
            cnt = cnt + 1

        cnt = cnt + 1

    # matrix Sv
    cnt = 0
    for train in trains:
        route = data.get(train)

        for i in range(0, len(route)):
            if (i != (len(route) - 1)):
                if (route[i] > route[i+1]):
                    segment = route[i+1] + route[i]
                else:
                    segment = route[i] + route[i+1]
            else:
                if (route[i] > route[0]):
                    segment = route[0] + route[i]
                else:
                    segment = route[i] + route[0]

            segment = train + segment
            Sv[trains_on_segments.index(segment)][cnt] = 1
            cnt = cnt + 1

        cnt = cnt + 1

    # matrica S = [Su; Sv; Sr; Sy]
    S = np.concatenate((Su, Sv, Sr, Sy), axis=0)

    Su = Su.astype(int)
    Sv = Sv.astype(int)
    Sr = Sr.astype(int)
    Sy = Sy.astype(int)
    S = S.astype(int)

    return [S, Su, Sv, Sr, Sy]

def get_Matrix_W(F, S):

    '''
    This function calculates matrix W. It gets matrices F and S as
    arguments and then calculates matrix W by formula W = transpose(S) - F
    and returns it as a result.
    '''

    W = np.transpose(S) - F

    return W

################################################################################################################
