# short-selling

TODO:
  Jessie: Dynamics
  Varad: Network modeling/generation


  c = number of commodities being traded

  Agent i has properties:

  u = agent i's utility function
  e = agent i's endowment (e is list with e[k] is amount of commodity k agent i has)
  endowment_plan = agent i's plan to sell
  p = list where p[k] agent i's price they sell commodity k at.
  x[j] = subplans with the vector of goods going from agent j to agent i (list of lists. each element of list is the vector of goods they plan to buy)

  budget_constraint[i] = sum over c
