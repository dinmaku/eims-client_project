<template>


  <div id="app">
    <router-view name="nav"></router-view> 
    <router-view></router-view> 
  </div>


</template>
  
  
  <script>
  export default{
    name: 'App',
   
    }
  
  
  </script>
  
  <style>
  #App {
    font-family:Verdana, Geneva, Tahoma, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
  }
  
  
  </style>
  