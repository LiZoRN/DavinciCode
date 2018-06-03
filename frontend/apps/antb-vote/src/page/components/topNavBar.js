import React, { Component } from 'react';
import { 
	ActionSheet,
	NavBar,
	Icon
 } from 'antd-mobile';


const logoImg = require('../../images/antb.png');
class TopNavBar extends Component {
  constructor(props){
    super(props)
    this.state = {
		title:this.props.title,
		showRC:this.props.showRC?this.props.showRC:false,
		back:this.props.back?this.props.back:-1
	}
  }
  showActionSheet = () => {
    const BUTTONS = [<div className='actionSheetBtn'><img src={logoImg} alt={logoImg}/>投票广场置顶</div>, '发送给朋友', '复制链接', '取消'];
    ActionSheet.showActionSheetWithOptions({
      options: BUTTONS,
      cancelButtonIndex: BUTTONS.length - 1,
      //destructiveButtonIndex: BUTTONS.length - 2,
      // title: 'title',
      //message: 'I am description, description, description',
      //maskClosable: true,
      //'data-seed': 'logId',
    },
    (buttonIndex) => {
      this.setState({ clicked: BUTTONS[buttonIndex] });
    });
  }
  render() {
    return (
	  <NavBar
	    mode='light'
	    leftContent = {[
		  <Icon key='navbar_l' type='left' color='gray' onClick={()=>{window.history.go(this.state.back)}}/>
	    ]}
	    rightContent = {this.state.showRC?[
		  <Icon key='navbar_r' type='ellipsis' color='gray' onClick={this.showActionSheet} />
	    ]:[]}
	    style={{backgroundColor:"#f8f8f8",height:40,position:'fixed',top:0,left:0,right:0,zIndex:10}}
	  >
		<strong>{this.state.title}</strong>
	  </NavBar>
    );
  }
}

export default TopNavBar;
