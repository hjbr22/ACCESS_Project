

// rps for graphical jobs
const graphicalRps = ['ACES', 'Bridges-2', 'DARWIN', 'Delta', 'Expanse', 'FASTER', 'KyRIC', 'Stampede-2']

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
    
    //get the job classes
    let job_types;
    $.ajax({
        type:"GET",
        url:"/get_job_classes",
        success:function(response){
            job_types = response
            // autocomplete for selecting classes of jobs
            $("#job-type-text-input").autocomplete({
                source: job_types,
                select: function(event, ui){
                    $('#job-type-tag-container').append(
                        `<div class="tag" style="display: inline-block; margin: 2px;">
                            <span class="badge badge-primary" id="${ui.item.value}">${ui.item.value}
                            <a class="remove-tag" name="remove-tag" style="cursor:pointer; color: white; margin-left: 5px;">x</a>
                            </span>
                        </div>`)
                    this.value='';
                    let selected_jobs = $("input[name=job-class]").val()
                    let current_selection = ui.item.value
                    $("input[name=job-class]").val(selected_jobs.concat(",",current_selection))
                    return false;
                }
            })
        },
        error: function(error){
            console.log("Error: ", error)
        }
    })
        
    // remove the job class when 'x' is clicked
    $(document).on('click', '.remove-tag', function(){
        $(this).parents('.tag').remove()
    })

    $.ajax({
        type:"GET",
        url:"/get_software",
        success:function(response){
            softwareInfo = response
            // autocomplete for selecting software
            $("#software-text-input").autocomplete({
                source: softwareInfo,
                maxShowItems: 10,
                select: function(event, ui){
                    $('#software-tag-container').append(
                        `<div class="tag" style="display: inline-block; margin: 2px;">
                            <span class="badge badge-primary" id="${ui.item.value}">${ui.item.value}
                            <a class="remove-tag" name="remove-tag" style="cursor:pointer; color: white; margin-left: 5px;">x</a>
                            </span>
                        </div>`)
                    this.value='';
                    let selected_softwares = $("input[name=software]").val()
                    let current_selection = ui.item.value
                    $("input[name=software]").val(selected_softwares.concat(",",current_selection))
                    return false;
                }
            })
        },
        error: function(error){
            console.log("Error: ", error)
        }
    });

    // calculate scores when the form is submitted
    $("#submit-form").on("click", function(){
        form = document.getElementById("recommendation-form")
        formData = new FormData(form)
        var formIsValid = validateForm();
        if (formIsValid){
            calculate_score(formData).then(function(recommendation){
                display_score(recommendation);
                openModal();
            }).catch(function(error){
                console.log("error when calculating score: ", error)
            })
        }
        form.reset()
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
  
function openModal() {
    $("#submitModal").modal("show");
}