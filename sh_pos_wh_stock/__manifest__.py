# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name" : "POS Product Warehouse Quantity",
    "author" : "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",        
    "category": "point of sale",
    "summary": "POS Warehouse Quantity Module,Warehouse Available Stock App, Point Of Sale Warehouse Product Quantity, POS Warehouse Management, POS Inventory Management, Get Point Of Sale Stock Detail, See POS Available Stock QTY Odoo",
    "description": """Do you want to display warehouse product stock in the POS products? Your warehouse plays an important role in product sales. You have to make sure that the ordered goods are in stock. This module helps to display the available stock quantity of all products in the POS. Here you get the total product quantity and how much quantity available in each warehouse.Point Of Sale Product Warehouse Quantity odoo,POS Warehouse Quantity Module, Display Warehouse Available Stock, Point Of Sale Warehouse Product Quantity, POS Warehouse Management, POS Inventory Management, Get Point Of Sale Stock Detail, See POS Available Stock QTY Odoo,POS Warehouse Quantity Module,Warehouse Available Stock App, Point Of Sale Warehouse Product Quantity, POS Warehouse Management, POS Inventory Management, Get Point Of Sale Stock Detail, See POS Available Stock QTY Odoo""",       
    "version":"13.0.2",
    "depends" : ["base","web","point_of_sale"],
    "application" : True,
    "data" : [
        'views/pos_config_settings.xml', 
        'views/assets.xml',       
            ],            
    "images": ["static/description/background.png",],  
    "live_test_url": "https://youtu.be/WJI9awlgWi0", 
    "qweb": ["static/src/xml/pos.xml"],           
    "auto_install":False,
    "installable" : True,  
    "price": "25",
    "currency": "EUR"    
}
