document.addEventListener('DOMContentLoaded',()=>{
    let seethegenre = document.querySelector('#option');
    let distinct = document.querySelector('#choose_category_header');
    if(distinct != null)
    {
        seethegenre.addEventListener('change',(event)=>{
            let value = event.target.value;
            location.replace(`http://127.0.0.1:8000/mycontents${value}`);
        })
    }
    let temp_notif = document.querySelectorAll('.notif_class');
    for(let i=0;i<temp_notif.length;i++)
    {
        temp_notif[i].addEventListener('click',()=>{
            fetch(`/API_Notif/${temp_notif[i].id}`,{
                method:'PUT',
                body:JSON.stringify({
                    seen:true
                })
            })
            temp_notif[i].remove();
        })
    }
    let delete_contentcreator_content = document.querySelectorAll('.delete_contentcreator_content');
    for(let i=0;i<delete_contentcreator_content.length;i++)
    {
        delete_contentcreator_content[i].addEventListener('click',()=>{
            fetch(`/API_Delete/${delete_contentcreator_content[i].value}/${delete_contentcreator_content[i].id}`,{
                method:'PUT',
                body:JSON.stringify({
                    id:delete_contentcreator_content[i].id,
                    category:delete_contentcreator_content[i].value
                })
            })
            setTimeout(function(){
                document.location.reload();
             },1000);
        })
    }
})