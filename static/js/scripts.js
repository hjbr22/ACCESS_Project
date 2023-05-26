// ACCESS RPs
const RPs = [['aces',"ACES (Texas A&M)"], ["anvil","Anvil (Purdue)"], ["bridges","Bridges-2 (PSC)"],
["darwin","DARWIN (Delaware)"], ["delta","Delta (NCSA)"], ["expanse","Expanse (SDSC)"],
["faster","FASTER (SDSC)"], ["jetstream","Jetstream2 (IU)"], ["ookami","OOKAMI (Stonybrook)"],
["kyric","KyRIC (Kentucky)"], ["rockfish","Rockfish (JHU)"], ["stampede","Stampede-2 (TACC)"],
["ranch","RANCH (TACC)"], ["osg","Open Science Grid (OSG)"], ["osn","Open Storage Network (OSN)"]]

// RPs with Open on Demand or other GUIs
const rpWithGUI = ['aces', 'anvil', 'bridges', 'delta', 'expanse', 'faster', 'jetstream', 'stampede']
    
// fields of research
const fieldsAndRps = {"Biology":['bridges','stampede','expanse'], 
                "Chemistry":['bridges','stampede'], 
                "Physics":['bridges','stampede','expanse'], 
                "Computer Science":['bridges','stampede','expanse'], 
                "Civil Engineering":['jetstream','bridges'], 
                "Economics":['jetstream','expanse'],
                "Linguistics":['osg'], 
                "History":['osg'], 
                "Agriculture":['kyric','anvil'], 
                "Medicine":['ookami','rockfish','bridges']}

// types of jobs
const jobTypeAndRps = {"Data Analytics":['delta', 'bridges', 'darwin'],
                 "Data Mining":['darwin'],
                 "NLP":['kyric'],
                 "Textual Analysis":['delta'],
                 "Modeling and Simulation":['delta'],
                 "Bioinformatics":['kyric','expanse'],
                 "Biophysics":['kyric','expanse'],
                 "Biochemistry":['kyric','expanse'],
                 "Fluid Dynamics":['delta'],
                 "Materials Science":['expanse'], 
                 "Image Processing":['darwin'], 
                 "Machine Learning":['delta','bridges','darwin'],
                 "Astronomic Science":['expanse'], 
                 "Digital Humanities":[], 
                 "Computational Chemistry":['expanse'], 
                 "Genomics":[], 
                 "Deep Learning":['delta'], 
                 "High Energy Physics":['expanse'],
                 "Virtual Machine":['jetstream'], 
                 "General":['stampede','darwin'], 
                 "Parallel":['stampede']}

// rps for graphical jobs
const graphicalRps = ['aces', 'bridges', 'darwin', 'delta', 'expanse', 'faster', 'kyric', 'stampede']

// CPU and GPU parallel RPs
const parallelRPs = ['bridges', 'darwin', 'delta', 'expanse', 'stampede']

// long term storage
const ltStorage ={'less-than-1':['delta', 'kyric', 'stampede'],
                  '1-10': ['anvil', 'darwin', 'faster', 'ookami', 'rockfish', 'ranch'],
                  'more-than-10':['aces', 'osn', 'jetstream', 'expanse', 'bridges'],
                  'unsure':[]}

// temp storage
const tempStorage = {'less-than-1':['aces', 'faster', 'osg'],
                    '1-10':['darwin', 'delta', 'kyric', 'rockfish'],
                    'more-than-10':['anvil', 'ookami', 'stampede', 'expanse', 'jetstream', 'bridges'],
                    'unsure':[]}

// memory
const RPmemory = {'less-than-64':['aces', 'anvil', 'bridges', 'darwin', 'delta', 'expanse', 'faster', 'jetstream',
               'ookami', 'kyric', 'rockfish', 'stampede', 'osg'],
     '64-512':['anvil', 'stampede', 'delta', 'expanse', 'faster', 'rockfish', 'bridges', 'darwin'],
     'more-than-512':['kyric', 'jetstream', 'bridges', 'delta', 'darwin', 'expanse', 'rockfish'],
     'unsure':[]}

// Initialize scores for each RP
let rpScores = {'aces':0, 'anvil':0, 'bridges':0, 'darwin':0, 'delta':0, 'expanse':0, 'faster':0, 'jetstream':0,
'ookami':0, 'kyric':0, 'rockfish':0, 'stampede':0, 'ranch':0, 'osg':0, 'osn':0}



$(document).ready(function(){ 

    // populate the experience with ACCESS providers options
    for (let i = 0; i < RPs.length; i++){
        $("#access-rps").append(
            $(`<div class="form-check">
                <input class="form-check-input used-rps" type="checkbox" id="${RPs[i][0]}-option-rp" value="${RPs[i][0]}">
                <label class="form-check-label" for="${RPs[i][0]}-option-rp">${RPs[i][1]}</label> 
               </div>`)
        )
    }

    // populate the field of research dropdown
    fields = Object.keys(fieldsAndRps).sort()
    for (let i = 0; i < fields.length; i++){
        $("#field-dropdown-options").append(
            $(`<div class="form-check dropdown-item">
            <input class="form-check-input" type="checkbox" id="${fields[i].split(' ').join('-').toLocaleLowerCase()}-option" value="${fields[i]}">
            <label class="form-check-label" for="${fields[i].split(' ').join('-').toLowerCase()}-option">${fields[i]}</label> 
            </div>`)
        )
    }

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


    /////
    // Recommending RPs
    ////

    // show the scores
    display_score()

    console.log(rpScores)

    // calculate scores when the form is submitted
    $("#submit-form").on("click", function(){
        calculate_score()
    })

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
        rpScores['jetstream'] += 1000
        console.log(rpScores)
    }

    //job length
    if($("input[name='job-run']:checked").val() == 1){
        console.log("runs forever")
        rpScores['jetstream'] += 1000
        console.log(rpScores)
    }

    // virtual machine
    if($("input[name='vm']:checked").val() == 1){
        console.log("needs vm")
        rpScores['jetstream'] += 1000
        console.log(rpScores)
    }

    console.log(rpScores)
    display_score()
}

function decrease_score(rp){
    rpScores[rp] -= 1
    console.log(rpScores)
}