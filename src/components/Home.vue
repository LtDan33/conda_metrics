<template>
  <div class="hello">
    <img src='@/assets/conda.png'/>
    <p>Test the {{poll}} things</p>
    <br/>
      <!-- {{ data }} -->
    <hr/>
    <h3>Open Issues</h3>
    <p v-if="messages.length === 0">No Messages</p>
  </div>

</template>


<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: "Messages",
  data() {
    return {
      subject: "",
      msgBody: "",
    };
  },
  computed: mapState({
    messages: state => state.messages.messages
  }),
  methods: mapActions('messages', [
    'addMessage',
    'deleteMessage'
  ]),
  created() {
    this.$store.dispatch('messages/getMessages')
  }
};

module.exports = {
  props: ['data']
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
hr {
  max-width: 65%;
}

.msg {
  margin: 0 auto;
  max-width: 30%;
  text-align: left;
  border-bottom: 1px solid #ccc;
  padding: 1rem;
}

.msg-index {
  color: #ccc;
  font-size: 0.8rem;
  /* margin-bottom: 0; */
}

img {
  width: 250px;
  padding-top: 50px;
  padding-bottom: 50px;
}

</style>
