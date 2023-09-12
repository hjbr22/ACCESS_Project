//Import tagify objects for event listeners     
import { fieldTagify, jobTagify, softwareTagify,
        addFieldTagify, addJobTagify, addSoftwareTagify,
        hideAddField, showAddField,
        hideAddJob, showAddJob,
        hideAddSoftware, showAddSoftware,
        fieldInWhitelist, jobInWhitelist, softwareInWhitelist } from "./tags.js";

$(document).ready(function(){ 
    $('html,body').animate({scrollTop:0},'fast')

    //event listeners for tagify fields
    fieldTagify.on("invalid", showAddField);
    addFieldTagify.on("remove", hideAddField)
    .on("invalid", fieldInWhitelist);

    jobTagify.on("invalid", showAddJob);
    addJobTagify.on("remove", hideAddJob)
    .on("invalid", jobInWhitelist);

    softwareTagify.on("invalid", showAddSoftware);
    addSoftwareTagify.on("remove", hideAddSoftware)
    .on("invalid", softwareInWhitelist);

    //initialize tooltips
    $('[data-toggle="tooltip"]').tooltip()

    // calculate scores when the form is submitted
    $("#submit-form").on("click", function(){
        var form = document.getElementById("recommendation-form")
        let formIsValid = validateForm() 
        if (formIsValid){
            let formData = get_form_data(form);
            calculate_score(formData).then(function(recommendation){
                if (!(recommendation === "{}")){
                    display_score(recommendation);
                    find_top_three(recommendation);
                    openModal(recommendation);
                    form.reset()
                }else{
                    let alertMsg = "Not enough information to make recommendation. Please provide a more detailed response"
                    showAlert(alertMsg)
                }
            }).catch(function(error){
                console.log("error when calculating score: ", error)
            })
        }
        else
        {
            let alertMsg = "Please fill out all of the required fields"
            showAlert(alertMsg)
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

    //Show GUI checkboxes if user needs GUI
    $('input[name="gui-needed"]').change(function(){
        if ($(this).val() === '1'){
            $('.hide-gui').removeClass('d-none').show();
        } else {
            $('.hide-gui').addClass('d-none').hide();
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

    $("#submitModal").on('hidden.bs.modal',function(e){
        location.reload();
    })

});

function showAlert(alertMsg){
    $("#alert-div").append(
        `<div class="alert alert-danger alert-dismissible fade show" id="alert" role="alert">
            ${alertMsg}
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>`
    )
    $("#alert").fadeTo(2000, 500).slideUp(1000, function(){
        $("#alert").slideUp(1000);
        $("#alert").alert('close')
    });
    $('html,body').animate({scrollTop:0},'fast')
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
                $(`[name=${name}]`).addClass("is-invalid")
            }else{
                $(`[name=${name}]`).removeClass("is-invalid")
            }
         }else{
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

    //Set research field tags and added tags
    let fieldTagValues = fieldTagify.value.map(tag => tag.value)
    formData.set('research-field', fieldTagValues)
    let fieldAddTags = addFieldTagify.value.map(tag => tag.value)
    formData.set('add-field-tags', fieldAddTags)

    //Set software tags and added tags
    let softwareTagValues = softwareTagify.value.map(tag => tag.value)
    formData.set('software', softwareTagValues)
    let softwareAddTags = addSoftwareTagify.value.map(tag => tag.value)
    formData.set('add-software-tags', softwareAddTags)

    //Set job class tags and added tags
    let jobTagValues = jobTagify.value.map(tag=>tag.value)
    formData.set('job-class',jobTagValues)
    let jobAddTags = addJobTagify.value.map(tag => tag.value)
    formData.set('add-job-tags', jobAddTags)

    return formData
}

function calculate_score(formData){

    // get and process data from each input field
    let jsonData = {}
    formData.forEach(function(value,key){
        if (key == "used-hpc" || key == "used-gui"){
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
    var parsedScores = JSON.parse(scores);
    var topThree=[];
    for (var rp in parsedScores) {
        if (parsedScores.hasOwnProperty(rp)) {
            var score = parsedScores[rp]['score'];
            var reasons = parsedScores[rp]['reasons'];
            topThree.push({ name: rp, score: score, reasons: reasons });
        }
    }
    console.log(topThree);

    topThree.sort(function(a, b) {
        return b.score - a.score;
    });

    topThree = topThree.slice(0, 3);
    for (let i=0; i<topThree.length; i++){
        $(`#box${i}-name`).text(topThree[i].name);
        $(`#box${i}`).removeClass('d-none').show();
        var tagsContainer = document.getElementById(`box${i}-suitability`);
        if (tagsContainer) {
            tagsContainer.innerHTML = ''; // Clear existing tags
            var tags = topThree[i].reasons;
            console.log(tags);
            if (tags) {
                tags.forEach(function(tag) {
                var tagElement = document.createElement('div');
                tagElement.classList.add('tag');
                tagElement.textContent = tag;
                tagsContainer.appendChild(tagElement);
                });
            }
        }
    }
}
//function to show modal upon clicking submit button
function openModal() {
    $("#submitModal").modal("show");
}

//Listen to modal boxes for clicks. Expands upon clicks.
var boxes = document.querySelectorAll('.box');
boxes.forEach(function(box) {
    box.addEventListener('click', function() {
      this.classList.toggle('expand');
      });
    });