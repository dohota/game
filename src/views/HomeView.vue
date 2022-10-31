<template>
  <div class="home">
    <div class="total">
      <span class="title">怪物世界</span>
      <button class="menu">总纲</button>
      <button class="menu">地图系统</button>
      <button class="menu">单位系统</button>
      <button class="menu">文明系统</button>
      <button class="menu">产业系统</button>
      <button class="menu">交易系统</button>
      <button class="menu">内置解释器</button>
    </div>
    <div class="bar1">
      <button class="btn">  
        <img src="../assets/card.png" class="tu"><p class="mi">数据库</p><p class="i">游戏中的详细具体数据都在其中</p>
      </button>
      <button class="btn">
        <img src="../assets/ss.png" class="tu"><p class="mi">游戏开发全流程</p><p class="i">介绍游戏构思制作上线迭代的全流程</p>
      </button>
      <button class="btn">
        <img src="../assets/tank.png" class="tu"><p class="mi">游戏攻略</p><p class="i">教你游戏思路，玩法</p>
      </button>
    </div>
    <div class="bar2">
      <button class="btn">
        <img src="../assets/p.png" class="tu"><p class="mi">关于作者</p><p class="i">更加了解作者(含个人博客)</p>
      </button>
      <button class="btn">
        <img src="../assets/story.png" class="tu"><p class="mi">模型展览</p><p class="i">展示游戏中3D模型</p>
      </button>
      <button class="btn">
        <p class="mi">其它</p><p class="i">可以玩小游戏</p>
      </button>
    </div>
  </div>
</template>

<script>
export default{
  name:'HomeView',
  setup(){
    let a = "这个游戏体量很大，可以成为游戏中的经典，可能接近于元宇宙。对战，冒险，卡牌是主流的三个版本，其中我认为最好玩的就是冒险模式（类似我的世界）这些主流模式也会包含赛车，格斗和FPS模式。每个模式也分简易版,中等版和复杂版"
    let b = "对战模式就是玩家间互相pvp，互相合作与竞争，玩家间的阵营可以像三国杀那样"
    let c = "更注重探险，也可以对战，像矮人要塞一样"
    let d = ""
    let e = "像电影一样，但是可以选择情节，可以完成主线和支线的任务"
    let pp = ""
  }
}
</script>

<style lang="less" scoped>
.home{
  background-image: url("../assets/bg2.png");

  .total{
  background-color: black;
  .title{
    color: rgb(174, 226, 43);
    text-shadow: 5px 5px 5px #FF0000;
    font-size: xx-large;
    padding-left: 10px;
    cursor: grab;
  }
  .menu{
    background-color: blueviolet;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: whitesmoke;
    border-radius: 25px;
    font-size: large;
    text-shadow: 1px 1px 1px yellow;
    margin-left: 40px;
    cursor: pointer;
  }
  .menu:hover{
    background-color: white;
    color:black;
    transform: scale(0.85);
  }
}
  .bar1,.bar2{
    position: relative;
    display: flex;
    flex-direction: row;
  .btn{
    cursor: pointer;
    border: 5px dashed #FF5722;
    background:
    linear-gradient(to top, green, 10px, transparent 10px),
    linear-gradient(to right, green, 10px, transparent 10px),
    linear-gradient(to bottom, green, 10px, transparent 10px),
    linear-gradient(to left, green, 10px, transparent 10px);
    //background-origin: border-box;
    background-image: linear-gradient(rgb(196, 196, 250), rgb(82, 181, 190), rgb(35, 40, 169));
    margin-top: 15px;
    margin-bottom: 15px;
    margin-left: 15px;
    border-radius: 40px;
    width: 460px;
    height: 320px;
    .tu{
      cursor: pointer;
      position: relative;
      top: 2%;
      left:2%;
      height: 150px;
      width: 100px;
      margin-top: 10px;
      margin-left: 20px;
    }
    .mi{
      margin-top: 8px;
      margin-left: 10px;
      font-size: larger;
      font-family:Verdana, Geneva, Tahoma, sans-serif;
      background: linear-gradient(to right, rgb(238, 176, 176), rgb(28, 234, 28));//文字渐变色
      -webkit-background-clip: text;
      color: transparent;
    }
    .i{
      color:rgb(205, 50, 177);
    }
    .mi:hover{
      transform: scale(1.4);
      color:black;
    }
    .i:hover{
      transform: scale(1.6);
      color: aqua;
    }
    .tu:hover{
      transform: scale(0.7);
    }
  }
  .btn:hover{
    transform: scale(0.95);
  }
}
} 
</style>