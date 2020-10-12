There is no time limit to this exercise, and the exercise is intended to be relatively short. Please don’t spend more than a handful of hours on it.

Please write the code as you would if you were intending to put it into production. Please write in Python.

Oh, and don’t worry, we won’t really be asking you to write banking software!

# Specification
We’re going to be keeping track of financial transactions between different parties — people and organisations. In our system, these parties are identified by a simple string such as "john" or "supermarket", and you will be provided with a ledger of transactions that looks like this:

2015-01-16,john,mary,125.00
2015-01-17,john,supermarket,20.00
2015-01-17,mary,insurance,100.00

Note: You will need to generate the necessary data to demonstrate the capabilities of your program.

In this example, John pays Mary §125.00 (§ is our fictional currency) on the 16th of January, and the next day he pays the supermarket §20.00, and Mary pays her insurance company, which costs her §100.00.

Your task will be to write a software system that can process a ledger in this format, and provide access to the accounts of each of the named parties, assuming they all started with a balance of zero. For example, the supermarket has received §20.00, so that’s its balance. John has paid out §125.00 to Mary and §20.00 to the supermarket, so his balance is in debit by §145.00. In other words, his balance is §-145.00.
 
 Of course, there’s a twist, which is as follows. We’d like to be able to find out what each party’s balance is at a specified date. For example, Mary’s balance on the 16th of January is §0.00, but on the 17th it’s §125.00.

You don’t need to implement any kind of user interface for your program. We’ll experiment with your code in a REPL.
