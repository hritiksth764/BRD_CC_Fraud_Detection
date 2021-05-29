
# **CustomerClassification**

## Statement:

NCB (New Central Bank, Europe) having presence all across the world. 
They are basically into Core & Retail Banking Features. 
They have thousands of Customers, and most of the Customers are widely using **NCB's Credit Card (Master and Visa).**

On a Daily Basis Millions of Credit Card Transactions are taking place.
The main intent of NCB is to identify the fraudulent Transactions and keep close eye on 
Suspicious Transactions on daily basis


Goal:Generate excel file having 3 sheets which contains following information


Sheet1:
```
Name: UnsupportedCurrency

Column: Transaction_ID,Customer_ID,Amount,Currency,Customer_LastName,Customer_FirstName

```


Sheet2:
```
Name: RiskyCustomer

Column: Transaction_ID,Customer_ID,Amount,Currency,Customer_LastName,Customer_FirstName
```

Sheet3:
```
Name: TransactionsWithBadCustomerID

Column: Transaction_ID,Customer_ID,Amount,Currency Customer_LastName,Customer_FirstName
```
Note: This process should be automatic and daily job needs to be executed on a given stipulated time and final copy of Excel Should be sent over a mail to given customers email id.

## Transformation Logic

 <img width="658" alt="TR" src="https://user-images.githubusercontent.com/42655809/120060977-8d0d4e00-c078-11eb-8ba3-8ff5a7ace822.png">
 <img width="491" alt="TR2" src="https://user-images.githubusercontent.com/42655809/120060743-1d4a9380-c077-11eb-9d1c-94255a9d976f.png">
 <img width="672" alt="TR3" src="https://user-images.githubusercontent.com/42655809/120060779-4cf99b80-c077-11eb-8e7a-5e2b9e8027e7.png">
 <img width="725" alt="TR4" src="https://user-images.githubusercontent.com/42655809/120060767-3c492580-c077-11eb-94d2-b443ce398863.png"> 

## Usage
.confg

