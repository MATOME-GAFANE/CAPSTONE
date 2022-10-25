$(document).ready(function() {
    $('.filter_instituions').change(function(){
  
      filter_function();
      
      //calling filter function each select box value change
      
    });
  
    $('table tbody tr').show(); //intially all rows will be shown
  
    function filter_function(){
      $('table tbody tr').hide(); //hide all rows
      
      
      var institutionFlag = 0;
      var institutionValue = $('#input_institution').val();
  
      var locationFlag = 0;
      var locationValue = $('#input_location').val();
      
      
      //setting intial values and flags needed
      
     //traversing each row one by one
      $('table tr').each(function() {  
  
        
        var institutionTable = $(this).find('td:eq(0)').text().toLowerCase();
        institutionValue = institutionValue.toLowerCase();
        if(institutionValue == 0){   //if no value then display row
            institutionFlag = 1;
        }
        else if(institutionValue == institutionTable){ 
            institutionFlag = 1;       //if value is same display row
        }
        else{
            institutionFlag = 0;
        }
        
  
        var locationTable = $(this).find('td:eq(1)').text().toLowerCase();
        locationValue = locationValue.toLowerCase();
        if(locationValue == 0){   //if no value then display row
            locationFlag = 1;
        }
        //var str1 = $(this).find('td.primaryResearch').data('primaryResearch');
  
        else if(locationTable.indexOf(locationValue) > -1){  //parentString.indexOf(substring);
            locationFlag = 1;       //if value is same display row
        }
        else{
            locationFlag = 0;
        }
        
        
        if(institutionFlag && locationFlag){
          $(this).show();  //displaying row which satisfies all conditions
        }
        
    
    });
        
    }
  
  });
