import PropTypes from 'prop-types';
import React from 'react';
import autoBind from 'react-autobind';

class Pagination extends React.Component {
  constructor(props) {
    super(props);
    // autoBind(this, 'handleClick', 'handleMouseMove');
  }

  render() {
    const { props } = this;
    let totalItems = this.props.totalItems;
    let itemsPerPage = this.props.perPage;
    let selectedPage = this.props.selectedPage;

    let numPages = Math.min(10, totalItems / itemsPerPage);

    return (
        <div>
            Results per page: &nbsp;
            <select onChange={this.props.handlePerPageChange}>
                <option value="10" selected>10</option>
                <option value="25">25</option>
                <option value="50">50</option>
                <option value="100">100</option>
            </select> &nbsp;
            {Array.from({length: numPages}, (x, i) => i).map((pageNumber) => {
                let color = "black";
                if (pageNumber+1 == this.props.selectedPage)
                    color = "red"
                return <span style={{cursor: "pointer", color: color, margin: "0.5em"}} onClick={this.props.handlePageNumberChange}>{pageNumber+1}</span>
            })}
        </div>
    );
  }
}

export default Pagination;
