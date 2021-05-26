Product Weight
---------------

This module allow to capture product weight with quantity on inventory transactions and provides Weight in Hand stock. It also include to activate billing on weigth price instead of quantity.  

Modifications on Modules
-------------------------

the following modules will chagne after instalaltion of this module:

 - Product
 - Partner
 - Sale Order
 - Purchase Order
 - Inventory
 - Manufacturing
 
Partner
---------

the following modification will include in the partner page:

 - add flags to active "Price on Weight" on sale order and purchase order respectivly. 

Product
---------

the following modification include in product page:

 - add flag to enable product to capture weight with movements i.e is_product_weight
 
Sale Order
-----------

Maintain following functionlity on Sale Order:

 - Add Weight, Total Weight and price weight feilds on order line. Weight field should be related to product, Total weight and Price weight will change values when change in (product,quantity), all fields are editable fields. 
 - Price Weight field only display and required if billing in weight active for respective customer. 
 - Display weight, total weight and price weight in Print Quotation/Sale Order Reports
 - Security group to display weight fields
 - Display and calculate Delivered Weight and Invoiced Weight fields on Order Line

Purchase Order
---------------

Maintain following functionlity on Purchase Order:

 - Add Weight, Total Weight and price weight feilds on order line. Weight field should be related to product, Total weight and Price weight will change values when change in (product,quantity), all fields are editable fields. 
 - Price Weight field only display and required if billing in weight active for respective supplier. 
 - Display weight, total weight and price weight in Print RFQ/Purchase Order Reports
 - Display and calculate Delivered Weight and Invoiced Weight fields on Order Line
 
Billing
-----------

Maintain following functionlity on Customer Invoice and Vendor Bills:

 - Add Weight, Total Weight and price weight feilds on order line. Weight field should be related to product, Total weight and Price weight will change values when change in (product,quantity), all fields are editable fields. The values would inherit from respective order and remain changable on invoice. 
 - Price Weight field only display and required if billing in weight active for respective partner. 
 - Display weight, total weight and price weight in Print Customer Invoice/Vendor Bill Reports
 - Display and calculate Recived Weight and Billed Weight fields on Order Line
 
Inventory
-----------

Maintain following functionlity on Picking Documents:

 - Calcualted Total Weight on each picking movement
 - Calcualte Total weight on product move line for regular delivery and receipt documents
 -
 Total Weight feilds on stock move line order line. Weight field should be related to product, Total weight and Price weight will change values when change in (product,quantity), all fields are editable fields. The values would inherit from respective order and remain changable on invoice. 
 - Price Weight field only display and required if billing in weight active for respective partner. 
 - Display weight, total weight and price weight in Print Customer Invoice/Vendor Bill Reports
 - Display and calculate Recived Weight and Billed Weight fields on Order Line
 
 
Security Group
---------------

Maintain the following security groups to manage product weight functionality:

 - Add security group to display weight fields to user
        - Display Weight on SO, PO, MO and Picking
        - Display Price in Wieght on SO, PO


