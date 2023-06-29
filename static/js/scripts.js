// memory
const RPmemory = {'less-than-64':['ACES', 'Anvil', 'Bridges-2', 'DARWIN', 'Delta', 'Expanse', 'FASTER', 'Jetstream2',
               'OOKAMI', 'KyRIC', 'Rockfish', 'Stampede-2', 'Open Science Grid'],
     '64-512':['Anvil', 'Stampede-2', 'Delta', 'Expanse', 'FASTER', 'Rockfish', 'Bridges-2', 'DARWIN'],
     'more-than-512':['KyRIC', 'Jetstream2', 'Bridges-2', 'Delta', 'DARWIN', 'Expanse', 'Rockfish'],
     'unsure':[]}

$(document).ready(function(){ 

    // search the field of research dropdown
    $("#field-dropdown-search").on("keyup", function(){
        var value = $(this).val().toLowerCase();
        $("#field-dropdown-options .dropdown-item").filter(function(){
            $(this).toggle(($(this).text().toLowerCase().indexOf(value)>-1))
        })
    })

    // show the scores
    display_score()


    // // calculate scores when the form is submitted
    $("#submit-form").on("click", function(){
        var form = document.getElementById("recommendation-form")
        var formIsValid = validateForm();
        if (1){
            let formData = get_form_data(form);
            calculate_score(formData).then(function(recommendation){
                display_score(recommendation);
                openModal();
            }).catch(function(error){
                console.log("error when calculating score: ", error)
            })
            form.reset()
        }
    })

    $('input[name="hpc-use"]').change(function() {
        if ($(this).val() === '1') {
          $('.hide-hpc').removeClass('d-none').show();
        } else {
          $('.hide-hpc').addClass('d-none').hide();
        }
      });
    $('input[name="storage"]').change(function() {
        if ($(this).val() === '1') {
          $('.hide-data').removeClass('d-none').show();
        } else if ($(this).val() === '2') {
           $('.hide-data').removeClass('d-none').show(); 
        } else {
            $('.hide-data').addClass('d-none').hide();
        }
      });

});

function display_score(score){
    $("#rpScore").append(
        $(`
            <label class="form-check-label text-wrap" for=""> 
                ${score}
            </label>`
        )
        )
}

function get_form_data(form){
    let formData = new FormData(form)
    let softwareTagValues = softwareTagify.value.map(tag => tag.value)
    formData.set('software', softwareTagValues)
    let jobTagValues = jobTagify.value.map(tag=>tag.value)
    formData.set('job-class',jobTagValues)

    return formData
}

function calculate_score(formData){

    // get and process data from each input field
    let jsonData = {}
    formData.forEach(function(value,key){
        if (key == "used-hpc" || key == "research-field"){
            if (!jsonData[key]) {
                jsonData[key] = [value];
            } else {
                jsonData[key].push(value);
            }
        } else {
            jsonData[key]=value
        }
    });

    //calculating score from backend
    return new Promise(function(resolve,reject){
        $.ajax({
            type:"POST",
            url:"/get_score",
            data:JSON.stringify(jsonData),
            contentType:"application/json",
            success:function(recommendation){
                resolve(recommendation)
            },
            error:function(error){
                reject(error)
            }
        });
    });    
}

function validateForm() {
    var valid = 1;

    //Find elements based on required attribute
    var reqFields = $("[required]")
    
    reqFields.each(function(){
        //Find name for those elements
        var name = $(this).attr("name");
        
        //Find values from those names if name exists, otherwise
        //directly check value. If value on required question is
        //undefined, set valid to 0 and display error message.
        if (name){
            if ($(`input[name=${name}]:checked`).val() == undefined){
                valid = 0;
            }
        }else{
            if (!$(this).val()){
                valid = 0;
            }
        }
    });
    return valid;
}

//function to show modal upon clicking submit button
function openModal() {
    $("#submitModal").modal("show");
}