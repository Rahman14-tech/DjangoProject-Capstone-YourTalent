document.addEventListener('DOMContentLoaded',()=>{
    let seethegenre = document.querySelector('#option');
    let distinct = document.querySelector('#choose_category_header');
    if(distinct != null)
    {
        seethegenre.addEventListener('change',(event)=>{
            let value = event.target.value;
            location.replace(`http://127.0.0.1:8000/interest${value}`);
        })
    }
    let inun = document.querySelectorAll('.inun_button');
    if(inun !== null)
    {
        for(let i=0;i<inun.length;i++)
        {
            inun[i].addEventListener('click',()=>{
                if(inun[i].id === "uninterest_button")
                {
                    fetch('/API_Uninterest',{
                    method:'POST',
                    body:JSON.stringify({
                        Content_id:inun[i].value,
                        Category:document.querySelector('#choose_category_header').innerHTML
                    })
                    })
                    .then(response => response.json())
                    .then(result =>{
                        if(typeof result.success != "undefined")
                        {
                            document.querySelector('#success_view').style.display = 'block';
                            document.querySelector('#success_view').innerHTML = `${result.success}`;
                            document.querySelector('#failed_view').style.display = 'none';
                        }
                        else if(typeof result.error != "undefined")
                        {
                            document.querySelector('#failed_view').style.display = 'block';
                            document.querySelector('#failed_view').innerHTML = `${result.error}`;
                            document.querySelector('#success_view').style.display = 'none';
                        }
                        let the_card = document.querySelector(`#card${inun[i].value}`);
                        the_card.remove();
                    })
                }
                else if(inun[i].id === "interest_button")
                {
                    document.querySelector('#success_view').style.display = 'block';
                    document.querySelector('#success_view').innerHTML = `${result.success}`;
                    document.querySelector('#failed_view').style.display = 'none';
                    inun.innerHTML = "Uninterest";
                    inun.id = "uninterest_button";
                }
            })    
        }
    }
})