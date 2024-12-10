// static/js/vue_app.js

new Vue({
    el: '#app',
    data: {
        challenges: []  // Ce tableau contiendra les défis
    },
    mounted() {
        // Lorsque le composant est monté, récupérez les données via l'API
        this.fetchChallenges();
    },
    methods: {
        fetchChallenges() {
            // Faites une requête GET à l'API Django pour récupérer les défis
            fetch('/api/challenges/')
                .then(response => response.json())
                .then(data => {
                    this.challenges = data;  // Mettez à jour le tableau de défis
                })
                .catch(error => console.error('Erreur de récupération des défis:', error));
        }
    }
});
