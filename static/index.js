'use strict'

$(document).ready(async function(){
    await displayAllCookies()
    $("#cupcake-form").on("submit", createCupCake)
    $("#search-cupcake").on("submit", searchCupCake)
})

async function displayAllCookies(){
    let resp = await axios.get('/api/cupcakes')

    let $cupcakeList = $("#cupcakes-list")
    $cupcakeList.empty()

    for(let cupcake of resp.data.cupcakes){
        let {flavor: flavor, id: id, image: image} = cupcake
        let $liTag = $(`<li><h4>${flavor} </h4> <img src="${image}" width="200px" height="200px"></li>`)
        $cupcakeList.append($liTag)
    }
}

async function createCupCake(event){
    console.log("create cupcake")
    event.preventDefault()

    let newCupcake = {
        "flavor":$("#flavor-in-form").val(),
        "size" : $("#size-in-form").val(), 
        "rating":$("#rating-in-form").val(), 
        "image" : $("#image-in-form").val() 
    }
    console.log($("#flavor-in-form"))
    await axios.post("/api/cupcakes", newCupcake)
    await displayAllCookies()

}

async function searchCupCake(event){
    event.preventDefault()
    let $searchTerm = $("#search-term").val()
    
}