// RPs with Open on Demand or other GUIs
const rpWithGUI = ['ACES', 'Anvil', 'Bridges-2', 'Delta', 'FASTER', 'Jetstream2']
    
// fields of research
const fieldsAndRps = {"Biology":['Bridges-2','Stampede-2','Expanse'], 
                "Chemistry":['Bridges-2','Stampede-2'], 
                "Physics":['Bridges-2','Stampede-2','Expanse'], 
                "Computer Science":['Bridges-2','Stampede-2','Expanse'], 
                "Civil Engineering":['Jetstream2','Bridges-2'], 
                "Economics":['Jetstream2','Expanse'],
                "Linguistics":['Open Science Grid'], 
                "History":['Open Science Grid'], 
                "Agriculture":['KyRIC','Anvil'], 
                "Medicine":['OOKAMI','Rockfish','Bridges-2']}

// types of jobs
const jobTypeAndRps = {"Data Analytics":['Delta', 'Bridges-2', 'DARWIN'],
                 "Data Mining":['DARWIN'],
                 "NLP":['KyRIC'],
                 "Textual Analysis":['Delta'],
                 "Modeling and Simulation":['Delta'],
                 "Bioinformatics":['KyRIC','Expanse'],
                 "Biophysics":['KyRIC','Expanse'],
                 "Biochemistry":['KyRIC','Expanse'],
                 "Fluid Dynamics":['Delta'],
                 "Materials Science":['Expanse'], 
                 "Image Processing":['DARWIN'], 
                 "Machine Learning":['Delta','Bridges-2','DARWIN'],
                 "Astronomic Science":['Expanse'], 
                 "Digital Humanities":[], 
                 "Computational Chemistry":['Expanse'], 
                 "Genomics":[], 
                 "Deep Learning":['Delta'], 
                 "High Energy Physics":['Expanse'],
                 "Virtual Machine":['Jetstream2'], 
                 "General":['Stampede-2','DARWIN'], 
                 "Parallel":['Stampede-2']}

// rps for graphical jobs
const graphicalRps = ['ACES', 'Bridges-2', 'DARWIN', 'Delta', 'Expanse', 'FASTER', 'KyRIC', 'Stampede-2']

// CPU and GPU parallel RPs
const parallelRPs = ['Bridges-2', 'DARWIN', 'Delta', 'Expanse', 'Stampede-2']

// long term storage
const ltStorage ={'less-than-1':['Delta', 'KyRIC', 'Stampede-2'],
                  '1-10': ['Anvil', 'DARWIN', 'FASTER', 'OOKAMI', 'Rockfish', 'RANCH'],
                  'more-than-10':['ACES', 'Open Storage Network', 'Jetstream2', 'Expanse', 'Bridges-2'],
                  'unsure':[]}

// temp storage
const tempStorage = {'less-than-1':['ACES', 'FASTER', 'Open Science Grid'],
                    '1-10':['DARWIN', 'Delta', 'KyRIC', 'Rockfish'],
                    'more-than-10':['Anvil', 'OOKAMI', 'Stampede-2', 'Expanse', 'Jetstream2', 'Bridges-2'],
                    'unsure':[]}

// memory
const RPmemory = {'less-than-64':['ACES', 'Anvil', 'Bridges-2', 'DARWIN', 'Delta', 'Expanse', 'FASTER', 'Jetstream2',
               'OOKAMI', 'KyRIC', 'Rockfish', 'Stampede-2', 'Open Science Grid'],
     '64-512':['Anvil', 'Stampede-2', 'Delta', 'Expanse', 'FASTER', 'Rockfish', 'Bridges-2', 'DARWIN'],
     'more-than-512':['KyRIC', 'Jetstream2', 'Bridges-2', 'Delta', 'DARWIN', 'Expanse', 'Rockfish'],
     'unsure':[]}

// Initialize scores for each RP
let rpScores = {'ACES':0, 'Anvil':0, 'Bridges-2':0, 'DARWIN':0, 'Delta':0, 'Expanse':0, 'FASTER':0, 'Jetstream2':0,
'OOKAMI':0, 'KyRIC':0, 'Rockfish':0, 'Stampede-2':0, 'RANCH':0, 'Open Science Grid':0, 'Open Storage Network':0}

//Load tags.js into this file
import {jobTagify, softwareTagify, jobTagInput, softwareTagInput} from "./tags.js"

$(document).ready(function(){ 

    // search the field of research dropdown
    $("#field-dropdown-search").on("keyup", function(){
        var value = $(this).val().toLowerCase();
        $("#field-dropdown-options .dropdown-item").filter(function(){
            $(this).toggle(($(this).text().toLowerCase().indexOf(value)>-1))
        })
    })

    //Event listeners for job and software tags
    jobTagify.on('input', jobTagInput);
    softwareTagify.on('input', softwareTagInput);

    // show the scores
    display_score()


    // // calculate scores when the form is submitted
    $("#submit-form").on("click", function(){
        var formIsValid = validateForm();
        if (formIsValid){
            // calculate_score();
            openModal();
            // display_score();

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

function increase_score(rp){
    rpScores[rp] += 1
}

function display_score(){
    $("#rpScore").append(
        $(`
            <label class="form-check-label text-wrap" for=""> 
                ${JSON.stringify(rpScores, null, 2)}
            </label>`
        )
        )
}

function calculate_score(){

    //calculating score from backend




    //scores are reinitialized to 0 each time scores are caculated
    rpScores = {'ACES':0, 'Anvil':0, 'Bridges-2':0, 'DARWIN':0, 'Delta':0, 'Expanse':0, 'FASTER':0, 'Jetstream2':0,
        'OOKAMI':0, 'KyRIC':0, 'Rockfish':0, 'Stampede-2':0, 'RANCH':0, 'Open Science Grid':0, 'Open Storage Network':0}

    // has not used an HPC before
    if($("input[name='hpc-use']:checked").val() == 0){
        for (let i=0; i < rpWithGUI.length; i++ ){
            increase_score(rpWithGUI[i])
        }
    }
    //if they have used an HPC before
    else if ($("input[name='hpc-use']:checked").val() == 1){ 
        // if they have used an ACCESS hpc before
        $(".used-rps:checkbox:checked").each(function(){
            increase_score($(this).val())
        })
    }
    
    // field of research
    $("input[id$='-option']:checked").each(function(){
        selectedField = $(this).val()
        for (let i=0; i<fieldsAndRps[selectedField].length; i++){
            increase_score(fieldsAndRps[selectedField][i])
        }
    })

    // type of job
    $(".badge").each(function(){
        selectedJob = $(this).attr('id')
        for (let i=0; i<jobTypeAndRps[selectedJob].length; i++){
            increase_score(jobTypeAndRps[selectedJob][i])
        }
    })
    
    // needs to store data on RP
    let needStorage = $("input[name='storage']:checked").val();
    if(needStorage == 1 || needStorage == 2){ //0 = no, 1 = yes, 2 = i don't know

        // long-term storage
        var ltStorageSelection = $("input[name='long-term-storage']:checked").val()
        if(ltStorageSelection){
            supportingRps = ltStorage[ltStorageSelection]
            for (let i=0; i < supportingRps.length; i++){
                increase_score(supportingRps[i])
            }
        }

        // temp storage
        var tempStorageSelection = $("input[name='temp-storage']:checked").val()
        if(tempStorageSelection){
            supportingRps = tempStorage[tempStorageSelection]
            for (let i=0; i < supportingRps.length; i++){
                increase_score(supportingRps[i])
            }
        }
    }


    // memory
    var memSelection = $("input[name='memory']:checked").val()
    if(memSelection){
        supportingRps = RPmemory[memSelection]
        for (let i=0; i < supportingRps.length; i++){
            increase_score(supportingRps[i])
        }
    }


    // libraries and packages

    // graphical component
    if($("input[name='graphics']:checked").val() == 1){
        for (let i=0; i<graphicalRps.length; i++){
            increase_score(graphicalRps[i])
        }
    }

    //CPU and GPU parallel
    if($("input[name='cpu-gpu-parallel']:checked").val() == 1){
        for (let i=0; i<parallelRPs.length; i++){
            increase_score(parallelRPs[i])
        }
        rpScores['Jetstream2'] += 1000
    }

    //job length
    if($("input[name='job-run']:checked").val() == 1){
        rpScores['Jetstream2'] += 1000
    }

    // virtual machine
    if($("input[name='vm']:checked").val() == 1){
        rpScores['Jetstream2'] += 1000
    }

}

function decrease_score(rp){
    rpScores[rp] -= 1
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