import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def map_vote_values_to_numeric(vote_data):
    # Replace Ayes and Yeas and Yeses with 1, Nos and Nays with -1
    vote_data = vote_data.replace('Aye', 1).replace('Yea', 1).replace('Yes', 1)
    vote_data = vote_data.replace('No', -1).replace('Nay', -1)
    # Replace neutral observations like Not Voting, Present with 0
    vote_data = vote_data.replace('Not Voting', 0).replace('Present', 0)

    # Drop all votes which haven't been cast to 1 or 0 or -1
    # Dropped: Name votes, like Speaker of the House.
    vote_data = vote_data[vote_data['vote_position'].isin([-1, 0, 1])]

    # Add dummy value 0 for missing dw_nominate scores
    if 'dw_nominate' in vote_data:
        vote_data['dw_nominate'].fillna(0, inplace=True)

    return vote_data


def generate_vote_matrix(df, sort_partisan=True):
    df = map_vote_values_to_numeric(df)
    row_pivots = ([df['dw_nominate']] if sort_partisan else []) + [df['name'], df['member_id'], df['party'], df['state']]
    column_pivots = [df['congress'], df['session'], df['date'], df['time'], df["roll_call"]]
    return pd.crosstab(row_pivots, column_pivots, values=df["vote_position"], aggfunc='sum')


def analyze_votes(votes):
    print "Creating correlation matrix...",
    corr = votes.transpose().corr()
    corr = corr.fillna(0)
    print "calculating eigenvectors, eigenvalues...",
    eigenvalues, eigenvectors = np.linalg.eig(corr)
    eigenvalues = np.real(eigenvalues) / len(corr)
    eigenvectors = eigenvectors.transpose()
    print "done."
    return corr, eigenvalues, eigenvectors


def show_corr_heat_map(corr):
    plt.imshow(corr.astype(float), cmap='hot', interpolation='nearest', clim=(-1, 1))
    plt.show()


def eigen_portfolio(e_vector, e_value, k, v):
    portfolio = map(lambda i: np.real(e_vector[k][i]) / np.sqrt(np.real(e_value[k])),
                    range(len(e_value)))
    # Normalize gross exposure to 1.0
    portfolio /= sum(np.absolute(portfolio))

    print "eigenportfolio", k, "gross=", sum(map(np.abs, portfolio)), "net=", sum(portfolio)

    # Cast to DataFrame
    portfolio = pd.DataFrame(data=portfolio, columns=['weight'], index=v.index)

    return portfolio


def show_eigen_portfolio(p, title):
    # p.index = p.index.str[:20]
    p.sort_values(by="weight").plot(kind='barh', legend=False)
    plt.title(title)
    plt.tick_params(axis='both', which='both', labelsize=6)
    # plt.tick_params(axis='both', which='both', labelsize=6, length=-40)
    plt.show()