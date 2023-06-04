
// RPs with Open on Demand or other GUIs
const rpWithGUI = ['ACES', 'Anvil', 'Bridges-2', 'Delta', 'Expanse', 'FASTER', 'Jetstream2', 'Stampede-2']
    
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



$(document).ready(function(){ 

    // search the field of research dropdown
    $("#field-dropdown-search").on("keyup", function(){
        var value = $(this).val().toLowerCase();
        $("#field-dropdown-options .dropdown-item").filter(function(){
            $(this).toggle(($(this).text().toLowerCase().indexOf(value)>-1))
        })
    })
    
    // autocomplete for selecting types of jobs
    $("#job-type-text-input").autocomplete({
        source: Object.keys(jobTypeAndRps),
        select: function(event, ui){
            $('#job-type-tag-container').append(
                `<div class="tag" style="display: inline-block; margin: 2px;">
                    <span class="badge badge-primary" id="${ui.item.value}">${ui.item.value}
                    <a class="remove-tag" name="remove-tag" style="cursor:pointer; color: white; margin-left: 5px;">x</a>
                    </span>
                </div>`)
            this.value='';
            return false;
        }
    })
        
    // remove the from job types when 'x' is clicked
    $(document).on('click', '.remove-tag', function(){
        $(this).parents('.tag').remove()
    })

    console.log(rpScores)

    // calculate scores when the form is submitted
    $("#submit-form").on("click", function(){
        calculate_score()
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

    //scores are reinitialized to 0 each time scores are caculated
    rpScores = {'ACES':0, 'Anvil':0, 'Bridges-2':0, 'DARWIN':0, 'Delta':0, 'Expanse':0, 'FASTER':0, 'Jetstream2':0,
        'OOKAMI':0, 'KyRIC':0, 'Rockfish':0, 'Stampede-2':0, 'RANCH':0, 'Open Science Grid':0, 'Open Storage Network':0}

    console.log($("input[name='hpc-use']:checked").val() == 0)
    // has not used an HPC before
    if($("input[name='hpc-use']:checked").val() == 0){
        console.log("has not used super computer")
        for (let i=0; i < rpWithGUI.length; i++ ){
            increase_score(rpWithGUI[i])
        }
    }
    //if they have used an HPC before
    else if ($("input[name='hpc-use']:checked").val() == 1){ 
        console.log("has used HPC before")
        // if they have used an ACCESS hpc before
        $(".used-rps:checkbox:checked").each(function(){
            console.log($(this).val())
            increase_score($(this).val())
        })
    }
    
    // field of research
    $("input[id$='-option']:checked").each(function(){
        selectedField = $(this).val()
        console.log("selections for field of research: ", selectedField)
        for (let i=0; i<fieldsAndRps[selectedField].length; i++){
            increase_score(fieldsAndRps[selectedField][i])
        }
    })

    // type of job
    $(".badge").each(function(){
        selectedJob = $(this).attr('id')
        console.log("selections for job types", selectedJob)
        for (let i=0; i<jobTypeAndRps[selectedJob].length; i++){
            increase_score(jobTypeAndRps[selectedJob][i])
        }
    })
    
    // needs to store data on RP
    let needStorage = $("input[name='storage']:checked").val();
    if(needStorage == 1 || needStorage == 2){ //0 = no, 1 = yes, 2 = i don't know

        // long-term storage
        ltStorageSelection = $("input[name='long-term-storage']:checked").val()
        console.log('hello')
        console.log($("input[name='long-term-storage']:checked").val())
        if(ltStorageSelection){
            supportingRps = ltStorage[ltStorageSelection]
            console.log("need long-term storage " + ltStorageSelection)
            for (let i=0; i < supportingRps.length; i++){
                increase_score(supportingRps[i])
            }
        }

        // temp storage
        tempStorageSelection = $("input[name='temp-storage']:checked").val()
        if(tempStorageSelection){
            supportingRps = tempStorage[tempStorageSelection]
            console.log("need temp storage " + tempStorageSelection)
            for (let i=0; i < supportingRps.length; i++){
                increase_score(supportingRps[i])
            }
        }
    }


    // memory
    memSelection = $("input[name='memory']:checked").val()
    console.log(memSelection)
    if(memSelection){
        supportingRps = RPmemory[memSelection]
        console.log("need memory " + memSelection)
        for (let i=0; i < supportingRps.length; i++){
            increase_score(supportingRps[i])
        }
    }


    // libraries and packages

    // graphical component
    if($("input[name='graphics']:checked").val() == 1){
        console.log($("input[name='graphics']:checked").val())
        console.log("has graphical component")
        for (let i=0; i<graphicalRps.length; i++){
            increase_score(graphicalRps[i])
        }
    }

    //CPU and GPU parallel
    if($("input[name='cpu-gpu-parallel']:checked").val() == 1){
        console.log("needs CPU GPU parallel")
        for (let i=0; i<parallelRPs.length; i++){
            increase_score(parallelRPs[i])
        }
        rpScores['Jetstream2'] += 1000
        console.log(rpScores)
    }

    //job length
    if($("input[name='job-run']:checked").val() == 1){
        console.log("runs forever")
        rpScores['Jetstream2'] += 1000
        console.log(rpScores)
    }

    // virtual machine
    if($("input[name='vm']:checked").val() == 1){
        console.log("needs vm")
        rpScores['Jetstream2'] += 1000
        console.log(rpScores)
    }

    console.log(rpScores)
    display_score()
}

function decrease_score(rp){
    rpScores[rp] -= 1
    console.log(rpScores)
}