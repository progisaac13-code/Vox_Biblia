let idParaDeletar = null;
let idParaEditar = null;

$(document).ready(function () {
    $('#tabela_de_oracoes').DataTable({
        select: true
    });
});

document.getElementById('area-oracao').style.display = 'none';
document.getElementById('myPray').style.display = 'block';

function editar_oracao() {
    const descricao = document.getElementById('descricao-edit').value;
    const id_categoria = document.getElementById('categoria-edit').value;
    const id_status = document.getElementById('status-edit').value;
    const privacidade = document.getElementById('privacidade-edit').value;

    fetch('/api/criar_oracao', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            id_oracao: idParaEditar,
            descricao: descricao,
            id_categoria: id_categoria,
            id_status: id_status,
            privacidade: privacidade,
            action: 'edição'
        })
    })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'Oração Criada') {
                document.getElementById('modal-edited').classList.remove("hidden");
                document.getElementById('modal-editar').classList.add('hidden');
            } else if (data.status === 'Não Logado!') {
                document.getElementById('liveToastBtn').click();
                document.querySelector('.text-toast').textContent = 'Oração não Editada!';
            }
        })
}


function criar_oracao() {

    const objetivo = document.getElementById('objetivo').value;
    const descricao = document.getElementById('descricao').value;
    const id_categoria = document.getElementById('categoria').value;
    const id_status = document.getElementById('status').value;
    const privacidade = document.getElementById('privacidade').value;
    const data_termino = document.getElementById('dataTermino').value;

    fetch('/api/criar_oracao', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            objetivo: objetivo,
            descricao: descricao,
            id_categoria: id_categoria,
            id_status: id_status,
            privacidade: privacidade,
            data_termino: data_termino,
            action: 'criar'
        })
    })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'Oração Criada') {
                document.getElementById('modal-created').classList.remove("hidden");
            } else if (data.status === 'Não Logado!') {
                document.getElementById('liveToastBtn').click();
                document.querySelector('.text-toast').textContent = 'Oração não adicionada!';
            }
        })
}

function mudarTabs(tab) {
    if (tab === 'myPray') {
        document.getElementById('area-oracao').style.display = 'none';
        document.getElementById('myPray').style.display = 'block';

        document.getElementById('btnMyPray').classList.add('active')
        document.getElementById('btnNewPray').classList.remove('active');

    } else if (tab === 'newPray') {
        document.getElementById('area-oracao').style.display = 'block';
        document.getElementById('myPray').style.display = 'none';

        document.getElementById('btnNewPray').classList.add('active');
        document.getElementById('btnMyPray').classList.remove('active');
    }
}

function excluir_oracao() {
    fetch('/api/oracoes/excluir', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            id: idParaDeletar
        })
    })
        .then(res => res.json())
        .then(data => {

            if (data.status === 'Oração Excluída com Sucesso!') {
                document.getElementById('liveToastBtn').click();

                document.querySelector('.text-toast').textContent = 'Oração Excluída com sucesso!';

                fecharModal('modal-delete');
                animacaoRemocao(idParaDeletar)

            } else {
                document.getElementById('liveToastBtn').click();
                document.querySelector('.text-toast').textContent = 'Só o usuário titular pode fazer a exclusão!';


            }
        })
}

function confimarExclusao(id) {
    idParaDeletar = id
    document.getElementById('modal-delete').classList.remove("hidden");
}

function confirmarEdicao(id) {
    idParaEditar = id

    fetch('/api/pegar_dados_oracao', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            id_oracao: id
        })
    })
        .then(res => res.json())
        .then(data => {
            document.getElementById('titlePray-edit').innerHTML = data.objetivo;
            document.getElementById('descricao-edit').value = data.descricao;

            document.getElementById('modal-editar').classList.remove("hidden");
        })

}

function fecharModal(cl) {
    document.getElementById(cl).classList.add('hidden');
}

function animacaoRemocao(id) {
    const linha = document.getElementById(`oracao-${id}`);

    linha.style.transition = 'all 0.3s ease';
    linha.style.opacity = "0";
    linha.style.transform = 'translateX(20px)';

    setTimeout(() => {
        linha.remove();
    }, 300)
}

