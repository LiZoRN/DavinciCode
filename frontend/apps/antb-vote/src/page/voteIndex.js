import React, { Component } from 'react';
import {Button,WingBlank} from 'antd-mobile';
import VoteImgList from './components/voteImgList';
import Footer from './components/footer';


			  
			  
			  
const logoImg = require('../images/antb.png');
const describeText = '奥特币投票表决系统，是基于区块链技术进行身份识别认证，以投票表决功能为主导，可以根据实际情况自定义投票内容。';
var votes = [
		{id:1,title:'陈漫',img:'http://imgs.aixifan.com/o_1cbrsvae053bo0r11arplk15ia1k.jpg',},
		{id:2,title:'魏天昊',img:'http://imgs.aixifan.com/o_1cdi1tr211j2312t13r91d41m6e1m.jpg',},
		{id:3,title:'野马',img:'http://imgs.aixifan.com/o_1cdi1tr211f24qamnmjte919ah1f.jpg',},
		{id:4,title:'Mr.Zhang',img:'http://imgs.aixifan.com/o_1cdi1tr22184dao61jb61f1p15du25.jpg',},
	];

class VoteIndex extends Component {
  render() {
    return (
	  <div >
		<WingBlank>
			<div className='logo'><img alt='logoImg' src={logoImg} /></div>
			<div className='describe'>{describeText}</div>
			<VoteImgList votes={votes}/>
			<Button href='/add' activeStyle={{backgroundColor:'#a28080',color:'white'}}>创建投票</Button>
		</WingBlank>
		<Footer />
	  </div>
    );
  }
}

export default VoteIndex;
