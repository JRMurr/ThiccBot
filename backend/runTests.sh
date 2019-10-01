#!/bin/sh
dockerize -wait tcp://postgres:5432 && py.test