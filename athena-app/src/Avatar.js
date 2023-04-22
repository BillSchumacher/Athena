// Avatar.js
import React from 'react';
import './Avatar.css';

const Avatar = ({ user }) => {
    if (!user) {
    return null;
    }
  const initials = user.name.split(' ').map((n) => n[0]).join('');

  return (
    <div className="avatar" title={user.name}>
      {initials}
    </div>
  );
};

export default Avatar;
