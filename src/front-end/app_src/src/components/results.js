import React from 'react';
import autoBind from 'react-autobind';
import { isNil } from 'lodash';
import Result from './result';

class Results extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
        results_list: [{"title": "t1", "url":"www.google.com"},{"title": "t2", "url":"www.google2.com"}],
        results_total: 0,
    }

    autoBind(
      this,
      'renderResults',
    );
  }

  renderResult(title, link) {
    
    return (
        <li style={{marginBottom: "2em" }}>
          <Result
            resultRenderer={this.props.resultRenderer}
            title={title}
            link={link}
            styles={this.props.styles}   
          />
        </li>
    );
  }

  render() {
    console.log("Rendering");
    return (
      <ul className={this.props.styles["result-ul"]}>
        {this.props.result_list.map(item => {
            return this.renderResult(item["title"], item["url"])
        })}
      </ul>
    );
  }
}

export default Results;
