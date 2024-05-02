import React, { useState } from "react";

function Pagination({ itemsPerPage, data, onPageChange }) {
//   debugger
  const [currentPage, setCurrentPage] = useState(1);
  //get data length, data is a list []
  const totalItems = data.length;

  const totalPages = Math.ceil(totalItems / itemsPerPage);

  function handleClick(pageNumber) {
    setCurrentPage(pageNumber);
    onPageChange(pageNumber);
  }

  const pageNumbers = [];
  for (let i = 1; i <= totalPages; i++) {
    pageNumbers.push(i);
  }

  return (
    <nav>
      <ul className="pagination" style={{backgroundColor: "white"}}>
        {pageNumbers.map((pageNumber) => (
          <li key={pageNumber} className="page-item">
            <a
              href="#"
              className={`page-link ${pageNumber === currentPage ? "active" : ""}`}
              style={{backgroundColor: "white", color: "black"}}
              onClick={() => handleClick(pageNumber)}
            >
              {pageNumber}
            </a>
          </li>
        ))}
      </ul>
    </nav>
  );
}

export default Pagination;