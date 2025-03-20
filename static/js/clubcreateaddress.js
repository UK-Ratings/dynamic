$(document).ready(function() {

  $('#validate-button').click(function(e) {
      e.preventDefault();  // Prevent the default action of the button

      var sourceForm = $('#form1');
      var targetForm = $('#form2');

      // Get all input, select, and textarea fields in the source form
      var fields = sourceForm.find('input, select, textarea');

      fields.each(function() {
          var fieldName = $(this).attr('name');  // Get the name of the field
          var fieldValue = $(this).val();  // Get the value of the field
//          alert('1 to 2 fieldName: ' + fieldName + ' fieldValue: ' + fieldValue);
          // Set the value of the field in the target form to the value of the field in the source form
          targetForm.find('input[name="' + fieldName + '"], select[name="' + fieldName + '"], textarea[name="' + fieldName + '"]').val(fieldValue);
//          var targetField = targetForm.find('input[name="' + fieldName + '"], select[name="' + fieldName + '"], textarea[name="' + fieldName + '"]');
//          targetField.val(fieldValue);
        });
  });

  $('#use1-button').click(function(e) {
      e.preventDefault();  // Prevent the default action of the button

      var sourceForm = $('#form1');
      var targetForm = $('#form3');

      // Get all input, select, and textarea fields in the source form
      var fields = sourceForm.find('input, select, textarea');

      fields.each(function() {
          var fieldName = $(this).attr('name');  // Get the name of the field
          var fieldValue = $(this).val();  // Get the value of the field

          // Set the value of the field in the target form to the value of the field in the source form
          targetForm.find('input[name="' + fieldName + '"], select[name="' + fieldName + '"], textarea[name="' + fieldName + '"]').val(fieldValue);
      });
  });

  $('#use2-button').click(function(e) {
      e.preventDefault();  // Prevent the default action of the button

      var sourceForm = $('#form2');
      var targetForm = $('#form3');

      // Get all input, select, and textarea fields in the source form
      var fields = sourceForm.find('input, select, textarea');

      fields.each(function() {
          var fieldName = $(this).attr('name');  // Get the name of the field
          var fieldValue = $(this).val();  // Get the value of the field
//          alert('2 to 3 fieldName: ' + fieldName + ' fieldValue: ' + fieldValue);

          // Set the value of the field in the target form to the value of the field in the source form
          targetForm.find('input[name="' + fieldName + '"], select[name="' + fieldName + '"], textarea[name="' + fieldName + '"]').val(fieldValue);
      });
  });
});
