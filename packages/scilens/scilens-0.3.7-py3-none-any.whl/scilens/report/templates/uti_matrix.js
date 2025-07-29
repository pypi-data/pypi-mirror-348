((w_1, undef) => {
//
// {
//   "datasets": [
//       {
//           "nb_lines": 8,
//           "nb_columns": 3,
//           "data": [...],
//           "x_values": [...],
//           "y_values": [...]
//       }
//   ],
//   "names": ["csv"],
//   "spectrograms": {"display": 1},
//   "frameseries": {"display": 1}
// }
//
function subtractMatrices(A, B) {
    // // check dimensions
    return A.map((row, i) =>
    row.map((v, j) => v - B[i][j])
  );
}
//
class Matrix {
  constructor(data, x, y, name, ref) {
    this.data = data; // Matrix data array[array[float]]
    this.x = x; // X-axis values array[float]
    this.y = y; // Y-axis values array[float]
    this.name = name; // string
    this.ref = ref; // Reference matrix data (optional) array[array[float]]
    // // Check if the matrix is valid (rectangular)
    // const rowLength = data[0].length;
    // if (!data.every(row => row.length === rowLength)) {
    //   throw new Error("All rows must have the same number of columns.");
    // }
    // // Check if x and y dimensions match the data
    // // check if ref has the same dimensions
  }
  subtract(other, name) {
    // // check dimensions
    // if (
    //   this.data.length !== other.data.length ||
    //   this.data[0].length !== other.data[0].length
    // ) { throw new Error("Matrices must have the same dimensions."); }
    return new Matrix(subtractMatrices(this.data, other.data), this.x, this.y, name);
  }
  ref_diff_data() {
    return subtractMatrices(this.data, this.ref);
  }
}
class MatrixGroup {
  constructor(arr, is_spectro, is_frameseries, has_ref) {
    this.arr = arr; // array of Matrix objects
    this.is_spectro = is_spectro;
    this.is_frameseries = is_frameseries;
    this.has_ref = has_ref;
  }
}
const MatrixMgmt = {
  groups: [],
  loadGlobal: function() {
    // load loop GLOBAL_VARS groups
    const g = GLOBAL_VARS.matrices;
    g.test.forEach((data, i) => {
      const group_data = [];
      const ref = g.reference[i];
      data.datasets.forEach((dataset, j) => {
        const mat = new Matrix(dataset.data, dataset.x_values, dataset.y_values, data.names[j], ref.datasets[j].data);
        group_data.push(mat);
      });
      const group = new MatrixGroup(group_data, Boolean(data.spectrograms), Boolean(data.frameseries), true);
      this.groups.push(group);
    });
    // IMPORTANT
    // Release Global
    delete GLOBAL_VARS.matrices;
    // Init
    this.groups.forEach((group, i) => {
      // Init Spectrograms
      if (group.is_spectro) {
        const spec = new Spectrograms(i, group.arr);
      }
      // Init Frameseries
    }
    );
  },
};
w_1.MatrixMgmt = MatrixMgmt;
})(window);
