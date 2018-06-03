import React, { Component } from 'react';
import { 
	Accordion,
	WingBlank,
	List
 } from 'antd-mobile';
import Footer from './components/footer';
import { Link } from 'react-router-dom';


const headImg = require('../images/headImg.png');
const affirm_f = require('../images/affirm_f.png');
const affirm_t = require('../images/affirm_t.png');

const myVoteIcon1 = require('../images/myVoteIcon1.png');
const myVoteIcon2 = require('../images/myVoteIcon2.png');
const myVoteIcon3 = require('../icon/myVoteIcon3.svg');
const myVoteIcon4 = require('../icon/myVoteIcon4.svg');
const myVoteIcon5 = require('../icon/myVoteIcon5.svg');


class MyVote extends Component {
  constructor(props) {  
    super(props);  
    this.state = { 
		isAffirm:false,
	}
  }
  componentDidMount() {

  }
  
  render() {
    return (
	  <div>
		<div className='headImgBox'>
		  <Link to='/personalInfo'>
		    <img src={headImg} alt='headImg' className='headImg'/>
		  </Link>
		  <img 
			alt='affirm' 
			className='affirm'  
		    src={this.state.isAffirm?affirm_t:affirm_f} 
			onClick={() =>{this.setState({isAffirm:!this.state.isAffirm})}}
		  />
		</div>
		<WingBlank >
		  <Accordion className="my-accordion" accordion >
            <Accordion.Panel header={<div >我发起的投票 <img src={myVoteIcon1} alt='myVoteIcon1' /></div>} >
              <List >
                <List.Item arrow="horizontal">投票活动 1</List.Item>
                <List.Item arrow="horizontal">投票活动 2</List.Item>
                <List.Item arrow="horizontal">投票活动 3</List.Item>
              </List>
            </Accordion.Panel>
            <Accordion.Panel header={<div >我暂存的投票<img src={myVoteIcon2} alt='myVoteIcon2' /></div>} >
              <List >
                <List.Item arrow="horizontal">投票活动 1</List.Item>
                <List.Item arrow="horizontal">投票活动 2</List.Item>
                <List.Item arrow="horizontal">投票活动 3</List.Item>
              </List>
            </Accordion.Panel>
            <Accordion.Panel header={<div >我参与的投票<img src={myVoteIcon3} alt='myVoteIcon3' /></div>} >
              <List >
                <List.Item arrow="horizontal">投票活动 1</List.Item>
                <List.Item arrow="horizontal">投票活动 2</List.Item>
                <List.Item arrow="horizontal">投票活动 3</List.Item>
              </List>
            </Accordion.Panel>
            <Accordion.Panel header={<div >我的钱包<img src={myVoteIcon4} alt='myVoteIcon4' /></div>} >
              <List >
                <List.Item arrow="horizontal">拥有币数</List.Item>
              </List>
            </Accordion.Panel>
            <Accordion.Panel header={<div >关于我们<img src={myVoteIcon5} alt='myVoteIcon5' /></div>} >
              <List >
                <List.Item arrow="horizontal">系统更新</List.Item>
                <List.Item arrow="horizontal">产品介绍</List.Item>
                <List.Item arrow="horizontal">投诉建议</List.Item>
              </List>
            </Accordion.Panel>
          </Accordion>
        </WingBlank>
		<Footer pageIndex={2}/>
      </div>
    );
  }
}

export default MyVote;
