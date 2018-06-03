import React, { Component } from 'react';
import {
	WingBlank,
	Button,
	Carousel,
	Toast
} from 'antd-mobile';
import TopNavBar from './components/topNavBar';
import CheckList from './components/checkList';



const nowTimeStamp = Date.now();

class VotePage extends Component {
  constructor(props) {  
    super(props);  
    this.state = { 
	  voteId:props.match.params.voteId,
	  vote:[],
	  loading:true,
	  imgHeight:1
	}
  }
  
  componentDidMount(){
    this.getVoteData()
  }
  
  getVoteData(){
	let vote ={
	  title:'广东最美城市评选活动',
	  describe:'广东省”最美城市“评选，快来为你的城市加油！',
	  imgSrcList:[
			  'http://imgs.aixifan.com/o_1cbrsvae053bo0r11arplk15ia1k.jpg',
			  'http://imgs.aixifan.com/o_1cdi1tr211j2312t13r91d41m6e1m.jpg',
			  'http://imgs.aixifan.com/o_1cdi1tr211f24qamnmjte919ah1f.jpg',
			  'http://imgs.aixifan.com/o_1cdi1tr22184dao61jb61f1p15du25.jpg',
			],
	  endDate:nowTimeStamp + Math.floor(Math.random(10)*24*3600*1000),
	  voted:false,
	  maximum:2,
	  shortList:[
	  	{id:0,name:'广州',votes:345,selected:false},
	  	{id:1,name:'深圳',votes:787,selected:false},
	  	{id:2,name:'汕头',votes:466,selected:false},
	  	{id:3,name:'韶关',votes:453,selected:false}
	  ],
	  userList:["","","","","","","","","","","","","","","","","","",]
	}
	this.setState({
      loading:false,
	  vote:vote
    })
  }
  getShortList = (shortList) => {
	let {vote} = this.state;
	vote.shortList = shortList;
	//console.log(shortList);
	this.setState({
      vote:vote
    })
　}
  formatDate(timeStamp,str){
	let date = new Date(timeStamp);
	return [
	  date.getFullYear(),
	  date.getMonth() > 9 ? date.getMonth() : '0' + date.getMonth(),
	  date.getDate() > 9 ? date.getDate() :'0' + date.getDate()
	].join(str);
  }
  submitBtnClick = () => {
	let {vote} = this.state;
	let count = vote.shortList.filter((item) => item.selected).length;
	if(count > vote.maximum){
	  Toast.info('最多只能选' + vote.maximum + '项');
	}else if(count === 0){
	  Toast.info('请至少选择一项。');
	}else{
	  let result = '你把票投给了 ';
	  vote.shortList.map((item) => {
		if(item.selected)result += item.name + '，';
		return false;
	  })
	  Toast.info(result.substring(0,result.length - 1) + ' 。');
	  vote.voted = true;
	  this.setState({
	    vote:vote
	  })
	}
  }
  
  renderShortList = (vote) => {
	if(vote.voted){
	  return <div style={style.shortList}>
	  	{vote.shortList.sort((a,b) => b.votes-a.votes).map((item,index) => 
	  	<div key={'shortItem'+index} style={style.shortItem}>
	  	  {index+1}、{item.name}
	  	  <div style={style.shortItemVotesBox}>票数：<span style={style.shortItemVotes}>{item.votes}</span></div>
	  	</div>
	  	)}
	  </div>
	}else{
	  return <div>
	    <CheckList shortList={vote.shortList} maximum={vote.maximum} toParent={this.getShortList.bind(this)} />
		<Button style={style.submitBtn} activeStyle={{backgroundColor:"gray"}}  onClick={this.submitBtnClick}>确认投票</Button>
	  </div>;
	}
  }
  render() {
    if(this.state.loading){
  	  return (
  	  	<div>loading</div>
  	  )
    }
	const {vote} = this.state;
	let votesSum = 0;
	vote.shortList.forEach((item,index) => {
		votesSum += item.votes;
	})
	
    return (
	  <div>
		<TopNavBar title={''} showRC={true}/>
		<WingBlank style={{paddingTop:50,marginBottom:30}}>
	      <div style={style.title}>{vote.title}</div>
	      <div style={style.titleUnderLine}></div>
		  <Carousel autoplay={false} infinite>
		    {vote.imgSrcList.map(val =>
			  <img 
			    key={val}
			    src={val} 
			    alt={vote.imgSrc} 
			    style={{height:this.state.imgHeight}}
				onLoad={() => {
                  // fire window resize event to change height
                  window.dispatchEvent(new Event('resize'));
                  this.setState({ imgHeight: 'auto' });
                }}
			  />
		    )}
		  </Carousel>
	      <div style={style.describe}>
	        {vote.describe} <br />
	        （说明：点击选项进行投票，结果于投票后可见）
	      </div>
	      <div style={style.info}>
	        <div style={style.infoItem}>候选数量<br />{vote.shortList.length}</div>
	        <div style={style.infoItem}>累计投票<br />{votesSum}</div>
	        <div style={style.infoItem}>关注度<br />999</div>
	      </div>
	      {this.renderShortList(vote)}
	      <div style={style.endDate}>投票截止日期：{this.formatDate(vote.endDate,'-')}</div>
	      <div>
	        <div style={{lineHeight:'30px'}}>已有{votesSum}人参与投票</div>
			<div style={style.userList}>
			  {vote.userList.map((item,index) =>
				<img key={'headImg' + index} style={style.userItemImg} src={vote.imgSrcList[3]} alt={vote.imgSrc} />
			  )}
			</div>
	      </div>
		</WingBlank>
      </div>
    );
  }
}
const style ={
  title:{
  	textAlign:"center",
	lineHeight:'28px',
  	fontSize:16,
  },
  titleUnderLine:{
  	borderTop:"1px solid #aaa",
  	width:80,
  	margin:"5px auto",
  	height:5
  },
  img:{
  	width:"100%",
  },
  describe:{
  	color:"#999",
  	fontSize:16,
  	textIndent:"2em",
  	lineHeight:"25px",
  	marginTop:10
  },
  info:{
  	backgroundColor:"white",
	padding:"12px 0",
	margin:"10px 0",
	overflow:"hidden"
  },
  infoItem:{
  	width:"33%",
  	fontSize:16,
	textAlign:"center",
	"float":"left",
	lineHeight:"30px"
  },	
  shortItem:{
  	backgroundColor:"white",
  	fontSize:18,
	padding:10,
	margin:"10px 0 0 0",
	lineHeight:"30px",
	position:'relative'
  },
  shortItemVotesBox:{
  	color:"#a17e7e",
  	position:'absolute',
	right:10,
  	fontSize:14,
	"top":10,
  },
  shortItemVotes:{
  	backgroundColor:"#a17e7e",
  	color:"#fff",
	textAlign:"center",
  	minWidth:60,
  	fontSize:12,
	display:'inline-block'
  },
  submitBtn:{
  	backgroundColor:"#0cbc0a",
	color:'white',
	marginTop:10,
  },
  endDate:{
	textAlign:"right",
	color:'#999',
	lineHeight:'40px',
  },
  userList:{
	backgroundColor:'white',
	padding:5,
	overflow:'hidden'
	
  },
  userItemImg:{
	height:30,
	width:30,
	borderRadius:'50%',
	'float':'left',
	margin:'5px'
	
  },
}
export default VotePage;
