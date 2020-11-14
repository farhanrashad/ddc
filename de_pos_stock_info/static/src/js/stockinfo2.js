odoo.define('pos_popup_button', function (require){
  'use_strict';
  /*
  In order to use ActionButtonWidget, which specified in Screens
  please start with downloading the screens widget
  */

 var screens = require('point_of_sale.screens');

//declare a new variable and inherit ActionButtonWidget

var PopupButton = screens.ActionButtonWidget.extend({
  /*
  Thus PopupButton contains all methods from ActionButtonWidget.
  Now we need to define Template for our button,
  where the type of button you can find in Qweb (see below)
  */

template: 'PopupButton',
  /*
  We also need to choose the Action,
  which which will be executed after we click the button.
  For this purpose we define button_click method, where
  where name - Button name; widget - Button object;
  condition - Condition, which calls the button to show up
  (in our case, setting on show_popup_button option in POS config).
  */

button_click: function () {
  this.gui.show_popup('confirm', {
    'title': 'Popup',
    'body': 'Opening popup after clicking on the button',
    });
    }
  });

screens.define_action_button({
  'name': 'popup_button',
  'widget': PopupButton,
  'condition': function () {
  return this.pos.config.popup_button;
    },
    });
return PopupButton;
});
