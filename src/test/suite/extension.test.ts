import * as assert from 'assert'
import {createConnection} from 'typeorm'
import 'reflect-metadata'

import {User} from '../../entity/User'

// You can import and use all API from the 'vscode' module
// as well as import your extension to test it
import * as vscode from 'vscode'
// import * as myExtension from '../../extension';

suite('Extension Test Suite', () => {
  vscode.window.showInformationMessage('Start all tests.')

  // test('Sample test', () => {
  //   assert.strictEqual(-1, [1, 2, 3].indexOf(5))
  //   assert.strictEqual(-1, [1, 2, 3].indexOf(0))
  // })

  test('DB', async () => {
    var sqlite3 = require('sqlite3').verbose()
    var db = new sqlite3.Database('/Users/a/git/treebeardtech/deeptest/debug/src/.coverage')

    db.serialize(function () {
      db.run('CREATE TABLE lorem (info TEXT)')

      var stmt = db.prepare('INSERT INTO lorem VALUES (?)')
      for (var i = 0; i < 10; i++) {
        stmt.run('Ipsum ' + i)
      }
      stmt.finalize()

      db.each('SELECT rowid AS id, info FROM lorem', function (err, row) {
        console.log(row.id + ': ' + row.info)
      })
    })

    db.close()
  })
})
