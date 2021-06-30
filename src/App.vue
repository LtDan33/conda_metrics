<template>
  <div id="app">
    <h1>Conda Metrics</h1>
    <div id="nav">
     <router-link :to="{ name: 'home' }">Home</router-link> |
     <router-link :to="{ name: 'resources' }">Resources</router-link> |
     <router-link :to="{ name: 'messages' }">ORM Test</router-link>
    </div>
    <router-view/>
  </div>
</template>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
