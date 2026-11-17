# minor-decisions
#### Video demo: (url)
#### Description: 
Minor decisions is a website that helps users make small decisions using decision trees. 

I decided to store the decision trees in a database. To do that, I first created a file called _schema.sql_ which creates five tables: trees, nodes, options, categories, and tree_categories. I wrote each tree in a separate json file, each tree contains the title, categories, the start node, every node associated with the tree, and their options. To load the trees into the database, I wrote _seed.py_ 