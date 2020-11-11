import React from 'react';
import ReactDOM from 'react-dom';
import autoBind from 'react-autobind';

import SearchBar from '../src/components/search-bar';
import Results from '../src/components/results';
import Pagination from '../src/components/pagination';

import {config} from '../config.json'

import styles from './style.css';
import words from './words.json';

import { Grid, Cell } from 'styled-css-grid'

class App extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            result_list: [],
            searchKeywords: "",
            suggestions: [],
            per_page: 10,
            page_number: 1,
            total_results: 0
        };

        autoBind(this, 'handleChange', 'handleClear', 'handleSelection', 'handleSearch', 'handlePerPageChange', 'handlePageNumberChange');
    }

    handleClear() {
        this.setState({
            suggestions: []
        });
    }

    handleChange(input) {
        
        // Do the rest call here    
        let this_ = this;
        let config_url = config.api_url;
        if (config_url.charAt(config_url.length-1) != "/" ) {
            config_url += "/";
        }

        console.log("CONF URL: " + config_url)

        let url = config_url + 'suggestion?keywords=' + input;
        fetch(url)
        .then((data) => {
            data.text().then(function(text) {
                data = JSON.parse(text);
                this_.setState({
                    suggestions: data
                });
            })
        })
        .catch(console.log);
    }

    handleSelection(value) {
        if (value) {
            console.info(`Selected "${value}"`);
        }
    }

    handleSearch(value) {
        if (value) {
            console.info(`Searching "${value}"`);

            this.makeTheCall(value, this.state.page_number, this.state.per_page)
        }
    }

    makeTheCall(keywords, page_number, per_page) {
        
        if (keywords == "") {
            this.setState({
                "page_number": page_number,
                "per_page": per_page
            })
            return;
        }
        let this_ = this;
    
        let url = config.api_url + '/search?keywords=' + keywords + '&per_page=' + per_page + '&page_number=' + page_number;
        console.log("Rendering results" + url);
      
        // Do the rest call here    
        if(url) {
          fetch(url)
          .then((data) => {
              data.text().then(function(text) {
                  console.log(text);
                  data = JSON.parse(text);
                  this_.setState({
                      "result_list": data.links,
                      "searchKeywords": keywords,
                      "per_page": per_page,
                      "page_number": page_number,
                      "total_results": data.total_links
                  })
              })
          })
          .catch(console.log)
        }
      }

    suggestionRenderer(suggestion, searchTerm) {
        return (
        <span>
            <span>{searchTerm}</span>
            <strong>{suggestion.substr(searchTerm.length)}</strong>
        </span>
        );
    }

    resultRenderer(title, link) {
        return (
            <li>
                <div className="result-title">{title}</div>
                <div className="result-link">{link}</div>
            </li>
        );
    }

    handlePerPageChange(value) {
        this.makeTheCall(this.state.searchKeywords, this.state.page_number, value.target.value)
    }

    handlePageNumberChange(value) {
        this.makeTheCall(this.state.searchKeywords, value.target.innerText, this.state.per_page)
    }

    render() {

        console.log(styles[0]);

        return (
            <div className="container">
                <div className="row">
                    <Grid columns={15} gap="2px" justifyContent="space-around">
                    <Cell width={1} height={2} center middle>WAH SEARCH</Cell>
                    <Cell width={6} height={2} center middle>
                        <SearchBar
                        autoFocus
                        renderClearButton
                        shouldRenderSearchButton
                        placeholder="Enter search text"
                        onChange={this.handleChange}
                        onClear={this.handleClear}
                        onSelection={this.handleSelection}
                        onSearch={this.handleSearch}
                        suggestions={this.state.suggestions}
                        suggestionRenderer={this.suggestionRenderer}
                        styles={styles}
                    />
                    </Cell>
                    </Grid>
                </div>
                <br></br><br></br>
                <div className="row">
                    <Results 
                        result_list={this.state.result_list}
                        resultRenderer={this.resultRenderer}
                        styles={styles}
                    />
                </div>
                <br></br><br></br>
                <div className="row">
                    <Pagination
                        handlePerPageChange={this.handlePerPageChange}
                        totalItems={this.state.total_results}
                        selectedPage={this.state.page_number}
                        perPage={this.state.per_page}
                        handlePageNumberChange={this.handlePageNumberChange}
                    />
                </div>
            </div>
        );
    }
}

ReactDOM.render(<App />, document.getElementById('root'));
