import PropTypes from 'prop-types';
import React from 'react';
import autoBind from 'react-autobind';

class Result extends React.Component {
  constructor(props) {
    super(props);
    // autoBind(this, 'handleClick', 'handleMouseMove');
  }

  render() {
    const { props } = this;

    return (
        <div>
            <div className={this.props.styles.result_title}>
                <a href={this.props.link}>{this.props.title} </a>
            </div>
            
            <div className={this.props.styles.result_link}>
            <a href={this.props.link}>{this.props.link}</a>
            </div>
        </div>
    );
  }
}

export default Result;
