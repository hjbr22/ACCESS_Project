// ACCESS RPs
const RPs = [['aces',"ACES (Texas A&M)"], ["anvil","Anvil (Purdue)"], ["bridges","Bridges-2 (PSC)"],
["darwin","DARWIN (Delaware)"], ["delta","Delta (NCSA)"], ["expanse","Expanse (SDSC)"],
["faster","FASTER (SDSC)"], ["jetstream","Jetstream2 (IU)"], ["ookami","OOKAMI (Stonybrook)"],
["kyric","KyRIC (Kentucky)"], ["rockfish","Rockfish (JHU)"], ["stampede","Stampede-2 (TACC)"],
["ranch","RANCH (TACC)"], ["osg","Open Science Grid (OSG)"], ["osn","Open Storage Network (OSN)"]]

// fields of research
const fields = ["Biology", "Chemistry", "Physics", "Computer Science", "Civil Engineering", "Economics",
   "Linguistics", "History", "Agriculture", "Medicine"].sort()

// types of jobs
const jobType = ["Data Analytics", "Data Mining", "NLP", "Textual Analysis", "Modeling and Simulation", "Bioinformatics",
                 "Biophysics", "Biochemistry", "Fluid Dynamics", "Materials Science", "Image Processing", "Machine Learning",
                 "Astronomic Science", "Digital Humanities", "Compuational Chemistry", "Genomics", "Deep Learning", "High Energy Physics",
                 "Virtual Machine", "General", "Parallel"]

// rps for graphical jobs
const graphicalRps = ['aces', 'bridges', 'darwin', 'delta', 'expanse', 'faster', 'kyric', 'stampede']

// CPU and GPU parallel RPs
const parallelRPs = ['bridges', 'darwin', 'delta', 'expanse', 'stampede-2']

// long term storage
const ltStorage ={'less-than-1':['delta', 'kyric', 'stampede'],
                  '1-10': ['anvil', 'darwin', 'faster', 'ookami', 'rockfish', 'ranch'],
                  'more-than-10':['aces', 'osn', 'jetstream', 'expanse', 'bridges']}

// temp storage
const tempStorage = {'less-than-1':['aces', 'faster', 'osg'],
                    '1-10':['darwin', 'delta', 'kyric', 'rockfish'],
                    'more-than-10':['anvil', 'ookami', 'stampede', 'expanse', 'jetstream', 'bridges']}

// memory
const RPmemory = {'less-than-64':['aces', 'anvil', 'bridges', 'darwin', 'delta', 'expanse', 'faster', 'jetstream',
               'ookami', 'kyric', 'rockfish', 'stampede', 'osg'],
     '64-512':['anvil', 'stampede', 'delta', 'expanse', 'faster', 'rockfish', 'bridges', 'darwin'],
     'more-than-512':['kyric', 'jetstream', 'bridges', 'delta', 'darwin', 'expanse', 'rockfish']}

// Initialize scores for each RP
let rpScores = {'aces':0, 'anvil':0, 'bridges':0, 'darwin':0, 'delta':0, 'expanse':0, 'faster':0, 'jetstream':0,
'ookami':0, 'kyric':0, 'rockfish':0, 'stampede':0, 'ranch':0, 'osg':0, 'osn':0}



$(document).ready(function(){ 

    // populate the experience with ACCESS providers options
    for (let i = 0; i < RPs.length; i++){
        $("#access-rps").append(
            $(`<div class="form-check">
                <input class="form-check-input used-rps" type="checkbox" id="${RPs[i][0]}-option" value="${RPs[i][0]}">
                <label class="form-check-label" for="${RPs[i][0]}-option">${RPs[i][1]}</label> 
               </div>`)
        )
    }

    // populate the field of research dropdown
    for (let i = 0; i < fields.length; i++){
        $("#field-dropdown-options").append(
            $(`<div class="form-check dropdown-item">
            <input class="form-check-input" type="checkbox" id="${fields[i].split(' ').join('-').toLocaleLowerCase()}-option" value="">
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
        source: jobType,
        select: function(event, ui){
            $('#job-type-tag-container').append(
                `<div class="tag" style="display: inline-block; margin: 2px;">
                    <span class="badge badge-primary">
                        ${ui.item.value}
                        <a class="remove-tag" style="cursor:pointer; color: white; margin-left: 5px;">x</a>
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
    $("#rpScore").append(
        $(`<label class="form-check-label" for=""> ${JSON.stringify(rpScores)}</label>`)
        )

    // console.log(rpScores)

    rpWithGUI = ['aces', 'anvil', 'bridges', 'delta', 'expanse', 'faster', 'jetstream', 'stampede']
    
    // calculate scores when the form is submitted
    $("#submit-form").on("click", function(){
        calculate_score()
    })

});

function increase_score(rp){
    rpScores[rp] += 1
    console.log(rpScores)
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

    // type of job

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
}

function decrease_score(rp){
    rpScores[rp] -= 1
    console.log(rpScores)
}