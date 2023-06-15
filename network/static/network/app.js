document.addEventListener('DOMContentLoaded', function(){
    refresh();
    [...document.querySelectorAll('#edit')].forEach(function(item) {
        item.addEventListener('click', function() {
            console.log(item.parentElement.innerHTML);
            let parent = item.parentElement;
            const children = parent.children;
            const id = parent.id;
            const title = children[0];
            const button = children[1];
            const likes = children[3];
            const time = children[4];
            const paragraph = document.querySelector(`#text${id}`)
            const text = paragraph.innerHTML;
            parent.innerHTML = "";
            let textarea = document.createElement('textarea');
            textarea.value = text;
            let save = document.createElement('button');
            save.innerHTML = "Save";
            save.className = "btn btn-outline-primary";
            save.addEventListener('click', function(){
                let parent = save.parentElement;
                let newchildren = parent.children;
                const body = newchildren[1].value;
                fetch(`/posts/${id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        content: body
                    })
                  })

                parent.innerHTML = "";
                const newbody = document.createElement('p');
                newbody.innerHTML = body;
                parent.append(title);
                parent.append(button);
                parent.append(newbody);
                parent.append(likes);
                parent.append(time);
            })

            parent.append(title);
            parent.append(textarea);
            parent.append(save);

        });
    });
});

function refresh(){
    [...document.querySelectorAll('#like')].forEach(function(item) {
        item.addEventListener('click', function() {
            like(item);
        }) });
    [...document.querySelectorAll('#unlike')].forEach(function(item) {
        item.addEventListener('click', function() {
            unlike(item);
        }) });
}

function like(item){
    let p = item;
    let parent = p.parentElement;
    const id = parent.id;
    const children = p.children;
    const likes_element = children[1];
    let likes = likes_element.innerHTML;
    likes ++;
    fetch(`/likes/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            likes: likes
        })
        })
    p.innerHTML=""
    p.id = "unlike"
    p.innerHTML = `<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-heart-fill" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
    <path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"/>
</svg>
<span>${likes}</span>`;
    refresh();
}

function unlike(item){
    let p = item;
    let parent = p.parentElement;
    const id = parent.id;
    const children = p.children;
    const likes_element = children[1];
    let likes = likes_element.innerHTML;
    likes --;
    fetch(`/likes/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            likes: likes
        })
        })
    p.innerHTML=""
    p.id = "like"
    p.innerHTML = `<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-heart" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
    <path fill-rule="evenodd" d="M8 2.748l-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"/>
</svg>
<span>${likes}</span>`;
    refresh();
}