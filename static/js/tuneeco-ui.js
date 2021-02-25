tuneecoUI = {

  showNotification: function(message, color = 'primary') {

    $.notify({
      icon: "now-ui-icons ui-1_bell-53",
      message: message

    }, {
      type: color,
      timer: 4000,
      placement: {
        from:  'top',
        align: 'right'
      }
    });
  }


};