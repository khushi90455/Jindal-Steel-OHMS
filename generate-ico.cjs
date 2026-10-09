const pngToIco = require('png-to-ico').default;
const fs = require('fs');

pngToIco('build/icon.png')
  .then(buf => {
    fs.writeFileSync('build/icon.ico', buf);
    console.log('Successfully created build/icon.ico');
  })
  .catch(console.error);
