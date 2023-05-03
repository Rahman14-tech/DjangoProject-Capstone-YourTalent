document.addEventListener('DOMContentLoaded',()=>{
    const countdown_auth = document.querySelector('#countdown_auth');
    let close = 5
    setInterval(()=>{
        countdown_auth.innerHTML -= 1
        if(countdown_auth.innerHTML === '0')
        {
            countdown_auth.style.display = 'none';
            let button_resend = document.createElement('button');
            button_resend.className = "btn btn-outline-secondary";
            button_resend.innerHTML = "Resend";
            button_resend.addEventListener('click',()=>{
                document.querySelector('#warning_resend').style.display = 'block';
                setInterval(()=>{
                    close -= 1
                    if(close === 0)
                    {
                        document.querySelector('#warning_resend').style.display = 'none';
                        setTimeout(function(){
                            document.location.reload();
                         },1000);
                    }
                },1000)
                fetch(`/authenticate_api/${username}`,{
                    method:'PUT',
                    body:JSON.stringify({
                        username:username
                    })
                })
            })
            let part_authenticate = document.querySelector('#the_form_part_auth');
            let child = part_authenticate.append(button_resend);
            let username = document.querySelector('#authenticate_button').value;
        }
    },1000)
})