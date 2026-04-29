function favoritar(id, id_usuario) {
    fetch('/api/favoritar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            id_usuario: id_usuario,
            id_v: id
        })
    })
        .then(res => res.json())
        .then(data => {
            icone = document.getElementById('icone-fav' + id);


            if (data.status === 'adicionado') {
                icone.classList.remove('fa-regular');
                icone.classList.add('fa-solid');
                icone.style.color = '#ff0000';
            } else if (data.status === 'removido') {
                icone.classList.remove('fa-solid');
                icone.classList.add('fa-regular');
                icone.style.color = '#f8fafc';
            } else if (data.status === 'Não Logado!') {
                document.getElementById('liveToastBtn').click();
                document.querySelector('.text-toast').textContent = 'Faça login para salvar versículos!';
            }
        })
}

const toastTrigger = document.getElementById('liveToastBtn')
const toastLiveExample = document.getElementById('liveToast')
if (toastTrigger) {
    const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample)
    toastTrigger.addEventListener('click', () => {
        toastBootstrap.show()
    })
}

function compartilhar(texto) {

    const mensagem = `✝️ Palavra de hoje \n

    *${texto}*\n

    Medite nessa palavra. Deus pode falar algo novo no seu coração através dela! 🙏
    *VOX BIBLIA* - Conectado ao Supremo Criador. 📖✨`;
    const url = `https://api.whatsapp.com/send?text=${encodeURIComponent(mensagem)}`;

    if (/Android|iPhone|iPad|iPod/i.test(navigator.userAgent)) {
        window.location.href = url;
    } else {
        window.open(url, '_blank');
    }

}

const myModal = new bootstrap.Modal(document.getElementById('ModalDeusFalar'))
myModal.show()

function gerarAudio(texto, id) {
    const player = document.getElementById('player');
    const url = `/tts?texto=${encodeURIComponent(texto)}&nome=versiculo_${id}`;

    player.src = url;
    player.play();
}

function typingEffect(element, text, delay = 60) {
    let i = 0;
    element.textContent = '';

    function digitar() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            setTimeout(digitar, delay);
        }
    }

    digitar();
}

function fecharModal(cl) {
    document.getElementById(cl).classList.add('hidden');
}