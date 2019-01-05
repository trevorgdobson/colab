from gcp_helpers import *
from analysis_helpers import *
import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

query = """
  SELECT 
    name, member_id, party, state,
    congress, session, date, time, roll_call, description,
    vote_position, dw_nominate
  FROM `congress.votes_senate_all`
  WHERE date > '2018-7-1'
  """
df = execute_query(query)

print "Loaded", len(df), "rows."

print df.head()
v = generate_vote_matrix(df, sort_partisan=True)
print v.head()


# Run PCA for voters
corr, eigenvalues, eigenvectors = analyze_votes(v)
show_corr_heat_map(corr)
# TODO: Iterate over time! Build a better process for this...
show_eigen_portfolio(eigen_portfolio(eigenvectors, eigenvalues, 0, v), "1st E.V. Eigenportfolio")
show_eigen_portfolio(eigen_portfolio(eigenvectors, eigenvalues, 1, v), "2nd E.V. Eigenportfolio")
show_eigen_portfolio(eigen_portfolio(eigenvectors, eigenvalues, 2, v), "3rd E.V. Eigenportfolio")
print "Done plotting."
plt.hist(filter(lambda l: l > 0.0000001, eigenvalues), bins=100)
plt.title("Density of States")
plt.show()


# Run PCA for bills
v = v.transpose()  # so that bills are rows
corr, eigenvalues, eigenvectors = analyze_votes(v)
show_corr_heat_map(corr)
show_eigen_portfolio(eigen_portfolio(eigenvectors, eigenvalues, 0, v), "1st E.V. Eigenportfolio")
show_eigen_portfolio(eigen_portfolio(eigenvectors, eigenvalues, 1, v), "2nd E.V. Eigenportfolio")
show_eigen_portfolio(eigen_portfolio(eigenvectors, eigenvalues, 2, v), "3rd E.V. Eigenportfolio")
plt.hist(filter(lambda l: l > 0.0000001, eigenvalues), bins=100)
plt.title("Density of States")
plt.show()

exit(0)
