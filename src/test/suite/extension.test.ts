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
    const connection = await createConnection()
    console.log('Inserting a new user into the database...')
    throw Error('boom')
    // const user = new User()

    // user.firstName = 'Timber'

    // user.lastName = 'Saw'
    // user.age = 25
    // await connection.manager.save(user)
    // console.log(`Saved a new user with id: ${user.id}`)

    // console.log('Loading users from the database...')
    // const users = await connection.manager.find(User)
    // console.log('Loaded users: ', users)
  })
})
