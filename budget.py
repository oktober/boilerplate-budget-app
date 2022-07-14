class Category:
  
  def __init__(self, budget_category):
    self.budget_category = budget_category
    self.ledger = []
    self.balance = 0

  def __str__(self):
    output_text = ""
    total = 0
    # prints the category centered between "*", up to 30 characters long
    output_text += f"{self.budget_category:*^30}\n"
    for transaction in self.ledger:
      # prints the first 23 characters of the description
      output_text += f"{transaction['description'][0:23]:23}" 
      # prints the amount right-aligned, with 2 decimal places and up to 7 characters
      output_text += f"{transaction['amount']:>7.2f}\n"
      total += transaction['amount']
    # prints the total amount of all transactions
    output_text += "Total: " + str(total)
    return output_text

  def deposit(self, amount, description=""):
    self.balance += amount
    self.ledger.append({"amount": amount, "description": description})
    
  def withdraw(self, amount, description=""):
    # check if balance has enough for withdrawal
    if self.check_funds(amount):
      self.balance -= amount
      amount = -abs(amount)
      self.ledger.append({"amount": amount, "description": description})
      return True
    return False

  def get_balance(self):
    return self.balance

  def transfer(self, amount, transfer_to):
    # withdraw from this category
    withdrawn = self.withdraw(amount, "Transfer to " + transfer_to.budget_category)
    if withdrawn:
      # deposit to the transfer_to category
      transfer_to.deposit(amount, "Transfer from " + self.budget_category)
      return True
    return False

  def check_funds(self, amount):
    if self.get_balance() < amount:
      return False
    return True

def create_spend_chart(categories):
  spent = {}
  num_of_categories = len(categories)
  total_spent = 0
  output_text = "Percentage spent by category\n"
  # calculate the percentage spent for each category
  for category in categories:
    category_total_spent = 0
    spent[category.budget_category] = {}
    # need to get only negative amounts from ledger
    for transaction in category.ledger:
      if transaction['amount'] < 0:
        category_total_spent += abs(transaction['amount'])
        total_spent += abs(transaction['amount'])
    spent[category.budget_category]['amount_spent'] = category_total_spent
    
  for category in categories:
    # divide the amount spent in each category by the total amount spent by all categories, rounding down to the nearest ten
    spent[category.budget_category]['percentage_spent'] = int(spent[category.budget_category]['amount_spent']/total_spent * 10) * 10

  # loop from 100 - 0 backwards, stepping by 10
  for i in range(100,-1,-10):
    output_text += str(i).rjust(3) + '| '
    for budget_category in spent:
      if spent[budget_category]['percentage_spent'] >= i:
        output_text += "o  "
      else:
        output_text += "   "
    output_text += "\n"

  output_text += " " * 4 + "-" * (len(spent) * 3) + "-\n"

  # get the length of the longest category name
  longestCategory = 0
  for category in categories:
    longestCategory = max(longestCategory, len(category.budget_category))

  # print out the category names vertically
  for i in range(longestCategory):
    output_text += " " * 5
    for category in categories:
      if len(category.budget_category) > i:
        output_text += category.budget_category[i] + "  "
      else:
        output_text += "   "
    # don't add a newline to the last iteration
    if longestCategory-1 > i:
      output_text += "\n"
    
  return output_text
