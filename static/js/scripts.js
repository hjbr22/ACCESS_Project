// memory
const RPmemory = {'less-than-64':['ACES', 'Anvil', 'Bridges-2', 'DARWIN', 'Delta', 'Expanse', 'FASTER', 'Jetstream2',
               'OOKAMI', 'KyRIC', 'Rockfish', 'Stampede-2', 'Open Science Grid'],
     '64-512':['Anvil', 'Stampede-2', 'Delta', 'Expanse', 'FASTER', 'Rockfish', 'Bridges-2', 'DARWIN'],
     'more-than-512':['KyRIC', 'Jetstream2', 'Bridges-2', 'Delta', 'DARWIN', 'Expanse', 'Rockfish'],
     'unsure':[]};

//Import tagify objects for event listeners     
import { jobTagify, softwareTagify, jobNoMatches, softwareNoMatches, hideAddJob, showAddJob, hideAddSoftware, showAddSoftware } from "./tags.js";


$(document).ready(function(){ 

    // search the field of research dropdown
    $("#field-dropdown-search").on("keyup", function(){
        var value = $(this).val().toLowerCase();
        $("#field-dropdown-options .dropdown-item").filter(function(){
            $(this).toggle(($(this).text().toLowerCase().indexOf(value)>-1))
        })
    });

    jobTagify.on("dropdown:noMatch", jobNoMatches)
    .on("add", hideAddJob)
    .on("remove", showAddJob);

    softwareTagify.on("dropdown:noMatch", softwareNoMatches)
    .on("add", hideAddSoftware)
    .on("remove", showAddSoftware);


    // // calculate scores when the form is submitted
    
    $("#submit-form").on("click", function(){
        var form = document.getElementById("recommendation-form")
        let formIsValid = validateForm() 
        if (formIsValid){
            let formData = get_form_data(form);
            calculate_score(formData).then(function(recommendation){
                display_score(recommendation);
                find_top_three(recommendation);
                openModal(recommendation);
            }).catch(function(error){
                console.log("error when calculating score: ", error)
            })
            form.reset()
        }
        else
        {
            $("#alert-div").append(
                `<div class="alert alert-danger alert-dismissible fade show" id="alert" role="alert">
                    Please fill out all of the required fields
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>`
            )
            $("#alert").fadeTo(2000, 500).slideUp(500, function(){
                $("#alert").slideUp(500);
                $("#alert").alert('close')
            });
            $('html,body').animate({scrollTop:0},'fast')
        }
        return false
    })

    //Show RPs if user has experience
    $('input[name="hpc-use"]').change(function() {
        if ($(this).val() === '1') {
          $('.hide-hpc').removeClass('d-none').show();
        } else {
          $('.hide-hpc').addClass('d-none').hide();
        }
      });
    //Show storage questions if user needs storage
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
                $(`[name=${name}]`).addClass("is-invalid")
            }else{
                $(`[name=${name}]`).removeClass("is-invalid")
            }
         }else{
            console.log("the value is ", $(this).val())
            console.log("this is of type", typeof($(this).val()))
            if($(this).val() != null){
                console.log(true)
            }else{
                console.log(false)
            }
            if (!$(this).val()){
                valid = 0;
                $(this).addClass("is-invalid")
            }else{
                $(this).removeClass("is-invalid")
            }
        }
    });

    return valid;
}

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

//function to parse JSON data a create a list of top three recommendations
function find_top_three(scores){
    var parsedScores =JSON.parse(scores);
    var topThree=[];
    for (var rp in parsedScores) {
    if (parsedScores.hasOwnProperty(rp)) {
        var score = parsedScores[rp];
        topThree.push({ name: rp, score: score });
    }
    }

    topThree.sort(function(a, b) {
    return b.score - a.score;
    });

    topThree = topThree.slice(0, 3);
    $('#box1-name').text(topThree[0].name);
    $('#score1').text(topThree[0].score);
  
    $('#box2-name').text(topThree[1].name);
    $('#score2').text(topThree[1].score);
  
    $('#box3-name').text(topThree[2].name);
    $('#score3').text(topThree[2].score);
    console.log('Text set')
}
//function to show modal upon clicking submit button
function openModal() {
    $("#submitModal").modal("show");
}

//Listen to modal boxes for clicks. Expands upon clicks.
var boxes = document.querySelectorAll('.box');
boxes.forEach(function(box) {
    box.addEventListener('click', function() {
      console.log('Box clicked!');
      this.classList.toggle('expand');
  
      // Update the top margin of score2 and 3 based on the "expand" state
      if (box.id === 'box1') {
        document.getElementById('score2').style.marginTop = this.classList.contains('expand') ? '180px' : '65px';
        document.getElementById('score3').style.marginTop = this.classList.contains('expand') ? '225px' : '110px';
        if (document.getElementById('box2').classList.contains('expand')){
          document.getElementById('score3').style.marginTop = this.classList.contains('expand') ? '340px' : '225px';
        }
      }
      else if (box.id ==='box2'){
        if (document.getElementById('box1').classList.contains('expand')){
          document.getElementById('score3').style.marginTop = this.classList.contains('expand') ? '340px' : '225px';
        }
        else{
          document.getElementById('score3').style.marginTop = this.classList.contains('expand') ? '225px' : '110px';
        }
      }
      });
    });